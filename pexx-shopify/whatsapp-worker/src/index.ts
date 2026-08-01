interface Env {
	META_WA_TOKEN: string;
	SHOPIFY_WEBHOOK_SECRET: string;
	WA_PHONE_NUMBER_ID: string;
	WA_TEMPLATE_ORDER_CONFIRMED: string;
	WA_TEMPLATE_ORDER_DISPATCHED: string;
	SHOPIFY_SHOP: string;
	WORKER_BASE_URL: string;
	POSTHOG_PROJECT_KEY: string;
	POSTHOG_HOST: string;
	// ponytail: all four below are optional — COD email confirm/cancel and PostHog
	// capture no-op (log only) until they're set. See AUTOMATION-PLAN.md for what's blocked.
	SHOPIFY_ADMIN_TOKEN?: string;
	COD_LINK_SECRET?: string;
	RESEND_API_KEY?: string;
	RESEND_FROM?: string;
}

const GRAPH_VERSION = "v20.0";
// ponytail: template language hardcoded to the WhatsApp Manager default. Update if templates are created in a different locale.
const TEMPLATE_LANGUAGE = "en_US";
const SHOPIFY_ADMIN_API_VERSION = "2025-01";
const COD_LINK_TTL_SECONDS = 48 * 60 * 60; // matches the 48h auto-cancel window in Shopify Flow

export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
		const url = new URL(request.url);

		if (request.method === "GET" && url.pathname === "/cod/confirm") {
			return handleCodLink(url, env, "cod-confirmed", "Thanks — your order is confirmed and on its way to dispatch.");
		}
		if (request.method === "GET" && url.pathname === "/cod/cancel") {
			return handleCodLink(url, env, "cod-cancelled", "Done — your order has been cancelled.");
		}

		if (request.method !== "POST") {
			return new Response("Not found", { status: 404 });
		}

		const rawBody = await request.text();
		const validHmac = await verifyShopifyWebhook(request, rawBody, env.SHOPIFY_WEBHOOK_SECRET);
		if (!validHmac) {
			return new Response("Invalid signature", { status: 401 });
		}

		if (url.pathname === "/webhooks/orders-create") {
			return handleOrderCreated(JSON.parse(rawBody), env, ctx);
		}

		if (url.pathname === "/webhooks/fulfillments-create") {
			return handleFulfillmentCreated(JSON.parse(rawBody), env, ctx);
		}

		if (url.pathname === "/webhooks/fulfillments-update") {
			return handleFulfillmentUpdated(JSON.parse(rawBody), env, ctx);
		}

		return new Response("Not found", { status: 404 });
	},
} satisfies ExportedHandler<Env>;

async function verifyShopifyWebhook(request: Request, rawBody: string, secret: string): Promise<boolean> {
	const header = request.headers.get("X-Shopify-Hmac-Sha256");
	if (!header) return false;

	const key = await crypto.subtle.importKey(
		"raw",
		new TextEncoder().encode(secret),
		{ name: "HMAC", hash: "SHA-256" },
		false,
		["sign"],
	);
	const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(rawBody));
	const computed = btoa(String.fromCharCode(...new Uint8Array(signature)));
	return computed === header;
}

async function handleOrderCreated(order: any, env: Env, ctx: ExecutionContext): Promise<Response> {
	const phone = extractPhone(order.phone, order.customer?.phone, order.shipping_address?.phone);
	const customerName = order.customer?.first_name || order.shipping_address?.first_name || "there";
	const orderNumber = order.name ?? `#${order.order_number}`;
	const total = `₹${order.total_price}`;

	if (phone) {
		await sendTemplate(env, ctx, order, phone, env.WA_TEMPLATE_ORDER_CONFIRMED, [customerName, orderNumber, total]);
	}

	if (isCashOnDelivery(order) && order.email) {
		await sendCodConfirmationEmail(env, order);
	}

	return new Response("ok");
}

async function handleFulfillmentCreated(fulfillment: any, env: Env, ctx: ExecutionContext): Promise<Response> {
	// ponytail: fulfillment webhook payload doesn't always include the customer phone directly.
	// If this keeps skipping in production, add a Shopify Admin API lookup by order_id here.
	const phone = extractPhone(fulfillment.destination?.phone);

	if (phone) {
		await sendTemplate(env, ctx, fulfillment, phone, env.WA_TEMPLATE_ORDER_DISPATCHED, [
			fulfillment.tracking_number || "—",
			fulfillment.tracking_url || "",
		]);
	}

	ctx.waitUntil(
		capturePosthog(env, "order_dispatched", distinctIdFor(fulfillment), {
			order_id: fulfillment.order_id,
			tracking_number: fulfillment.tracking_number,
		}),
	);

	return new Response(phone ? "ok" : "No phone on fulfillment, dispatched event still captured", { status: 200 });
}

async function handleFulfillmentUpdated(fulfillment: any, env: Env, ctx: ExecutionContext): Promise<Response> {
	if (fulfillment.shipment_status !== "delivered") {
		return new Response("Not a delivered update, skipped", { status: 200 });
	}

	ctx.waitUntil(
		capturePosthog(env, "order_delivered", distinctIdFor(fulfillment), {
			order_id: fulfillment.order_id,
		}),
	);

	// ponytail: delivered stays WhatsApp-free (native Shopify "Delivered" notification already
	// covers the customer). This is where the THANKYOU15 referral email goes out instead.
	ctx.waitUntil(sendReferralThankYouEmail(env, fulfillment.order_id));

	return new Response("ok");
}

const REFERRAL_SENT_TAG = "thankyou15-sent";

async function sendReferralThankYouEmail(env: Env, orderId: number): Promise<void> {
	if (!env.RESEND_API_KEY || !env.RESEND_FROM || !env.SHOPIFY_ADMIN_TOKEN) {
		console.log("Referral thank-you email skipped — RESEND_API_KEY/RESEND_FROM/SHOPIFY_ADMIN_TOKEN not configured yet");
		return;
	}

	const order = await getOrderForReferralEmail(env, orderId);
	if (!shouldSendReferralEmail(order)) return;

	const res = await fetch("https://api.resend.com/emails", {
		method: "POST",
		headers: {
			Authorization: `Bearer ${env.RESEND_API_KEY}`,
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			from: env.RESEND_FROM,
			to: order!.email,
			subject: "A 15% thank-you for spreading the word",
			html: referralThankYouEmailHtml({ customerName: order!.firstName || "there" }),
		}),
	});

	if (!res.ok) {
		console.error("Referral thank-you email failed", res.status, await res.text());
		return;
	}

	await tagOrder(env, orderId, REFERRAL_SENT_TAG);
}

type ReferralOrder = { email: string | null; firstName: string | null; tags: string[] } | null;

function shouldSendReferralEmail(order: ReferralOrder): order is NonNullable<ReferralOrder> & { email: string } {
	return Boolean(order?.email) && !order!.tags.includes(REFERRAL_SENT_TAG); // ponytail: dedupe against repeat "delivered" webhook fires
}

async function getOrderForReferralEmail(env: Env, orderId: number): Promise<ReferralOrder> {
	const res = await fetch(`https://${env.SHOPIFY_SHOP}/admin/api/${SHOPIFY_ADMIN_API_VERSION}/graphql.json`, {
		method: "POST",
		headers: {
			"X-Shopify-Access-Token": env.SHOPIFY_ADMIN_TOKEN!,
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			query: `query getOrder($id: ID!) {
				order(id: $id) { email customer { firstName } tags }
			}`,
			variables: { id: `gid://shopify/Order/${orderId}` },
		}),
	});

	if (!res.ok) {
		console.error("Shopify order lookup failed", res.status, await res.text());
		return null;
	}

	const json: any = await res.json();
	const order = json.data?.order;
	if (!order) return null;
	return { email: order.email, firstName: order.customer?.firstName ?? null, tags: order.tags ?? [] };
}

function referralThankYouEmailHtml(opts: { customerName: string }): string {
	const { customerName } = opts;
	return `
		<div style="background: #F3EDE3; padding: 40px 16px; font-family: Georgia, 'Times New Roman', serif;">
			<div style="max-width: 480px; margin: 0 auto; background: #FFFFFF; border: 1px solid #D8C7AD; border-radius: 6px; overflow: hidden;">

				<div style="background: #F3EDE3; padding: 32px 40px 22px; text-align: center; border-bottom: 1px solid #D8C7AD;">
					<div style="font-size: 22px; letter-spacing: 3px; color: #2B241F; font-weight: normal;">PEXX</div>
					<div style="margin-top: 6px; font-size: 11px; letter-spacing: 2px; color: #896F4E;">HAND BLOCK-PRINTED IN JAIPUR</div>
				</div>

				<div style="padding: 40px;">
					<div style="font-size: 11px; letter-spacing: 2px; color: #9E3B2F; margin-bottom: 10px;">A THANK-YOU FROM PEXX</div>
					<h1 style="font-size: 24px; line-height: 1.3; color: #2B241F; margin: 0 0 18px;">Thanks for bringing PEXX home, ${customerName}.</h1>
					<p style="font-size: 16px; line-height: 1.65; color: #4A413A; margin: 0 0 28px;">
						If you know someone who'd love a piece of hand block-printed Jaipur craft as much as you do, here's 15% off their gift to you — on your next order, no strings attached.
					</p>

					<div style="text-align: center; margin: 0 0 28px;">
						<div style="display: inline-block; border: 2px dashed #9E3B2F; border-radius: 6px; padding: 16px 36px; font-size: 22px; letter-spacing: 4px; color: #9E3B2F; font-weight: bold;">
							THANKYOU15
						</div>
					</div>

					<div style="text-align: center; margin-bottom: 8px;">
						<a href="https://shop.poddarexp.com" style="display: inline-block; background: #9E3B2F; color: #FFFFFF; text-decoration: none; font-size: 14px; letter-spacing: 1px; padding: 14px 36px; border-radius: 4px;">SHOP NOW</a>
					</div>
					<p style="text-align: center; font-size: 12px; color: #8A8078; margin: 14px 0 0;">Valid on your next order · one use per customer</p>
				</div>

				<div style="background: #F3EDE3; padding: 22px 40px; text-align: center; border-top: 1px solid #D8C7AD;">
					<div style="font-size: 12px; letter-spacing: 1px; color: #9E3B2F;">SHOP.PODDAREXP.COM</div>
				</div>

			</div>
		</div>
	`;
}

function distinctIdFor(record: any): string {
	const email = record.email || record.customer?.email;
	if (email) return email.toLowerCase();
	const phone = extractPhone(record.phone, record.destination?.phone, record.customer?.phone);
	return phone || `order-${record.order_id || record.id}`;
}

function extractPhone(...candidates: (string | undefined | null)[]): string | null {
	for (const raw of candidates) {
		if (!raw) continue;
		const digits = raw.replace(/[^\d+]/g, "");
		if (digits.startsWith("+")) return digits;
		if (digits.length === 10) return `+91${digits}`; // ponytail: India-only assumption, matches the store's current market
		if (digits.length > 10) return `+${digits}`;
	}
	return null;
}

async function sendTemplate(
	env: Env,
	ctx: ExecutionContext,
	sourceRecord: any,
	to: string,
	templateName: string,
	bodyParams: string[],
): Promise<void> {
	const res = await fetch(`https://graph.facebook.com/${GRAPH_VERSION}/${env.WA_PHONE_NUMBER_ID}/messages`, {
		method: "POST",
		headers: {
			Authorization: `Bearer ${env.META_WA_TOKEN}`,
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			messaging_product: "whatsapp",
			to,
			type: "template",
			template: {
				name: templateName,
				language: { code: TEMPLATE_LANGUAGE },
				components: [
					{
						type: "body",
						parameters: bodyParams.map((text) => ({ type: "text", text })),
					},
				],
			},
		}),
	});

	if (!res.ok) {
		console.error("WhatsApp send failed", res.status, await res.text());
		return;
	}

	ctx.waitUntil(capturePosthog(env, "whatsapp_message_sent", distinctIdFor(sourceRecord), { template: templateName }));
}

function isCashOnDelivery(order: any): boolean {
	const names: string[] = order.payment_gateway_names || [];
	return names.some((name) => /cash on delivery|\bcod\b/i.test(name));
}

// --- COD email confirm/cancel -----------------------------------------------------------

async function sendCodConfirmationEmail(env: Env, order: any): Promise<void> {
	if (!env.RESEND_API_KEY || !env.RESEND_FROM || !env.COD_LINK_SECRET) {
		console.log("COD confirmation email skipped — RESEND_API_KEY/RESEND_FROM/COD_LINK_SECRET not configured yet");
		return;
	}

	const orderNumber = order.name ?? `#${order.order_number}`;
	const customerName = order.customer?.first_name || order.shipping_address?.first_name || "there";
	const exp = Math.floor(Date.now() / 1000) + COD_LINK_TTL_SECONDS;
	const confirmUrl = await buildCodLink(env, "confirm", order.id, exp);
	const cancelUrl = await buildCodLink(env, "cancel", order.id, exp);

	const res = await fetch("https://api.resend.com/emails", {
		method: "POST",
		headers: {
			Authorization: `Bearer ${env.RESEND_API_KEY}`,
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			from: env.RESEND_FROM,
			to: order.email,
			subject: `Please confirm your COD order ${orderNumber}`,
			html: codConfirmationEmailHtml({ customerName, orderNumber, confirmUrl, cancelUrl }),
		}),
	});

	if (!res.ok) {
		console.error("COD confirmation email failed", res.status, await res.text());
	}
}

async function buildCodLink(env: Env, action: "confirm" | "cancel", orderId: number, exp: number): Promise<string> {
	const sig = await signCodToken(env.COD_LINK_SECRET!, orderId, exp);
	const params = new URLSearchParams({ order: String(orderId), exp: String(exp), sig });
	return `${env.WORKER_BASE_URL}/cod/${action}?${params.toString()}`;
}

async function signCodToken(secret: string, orderId: number, exp: number): Promise<string> {
	const key = await crypto.subtle.importKey(
		"raw",
		new TextEncoder().encode(secret),
		{ name: "HMAC", hash: "SHA-256" },
		false,
		["sign"],
	);
	const payload = `${orderId}.${exp}`;
	const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(payload));
	return bufferToBase64Url(signature);
}

function bufferToBase64Url(buf: ArrayBuffer): string {
	const base64 = btoa(String.fromCharCode(...new Uint8Array(buf)));
	return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function handleCodLink(
	url: URL,
	env: Env,
	tag: "cod-confirmed" | "cod-cancelled",
	successMessage: string,
): Promise<Response> {
	const orderId = url.searchParams.get("order");
	const exp = Number(url.searchParams.get("exp"));
	const sig = url.searchParams.get("sig");

	if (!orderId || !exp || !sig || !env.COD_LINK_SECRET) {
		return new Response("Invalid or unconfigured link", { status: 400 });
	}
	if (Date.now() / 1000 > exp) {
		return new Response(simpleHtmlPage("This link has expired. Please contact us on WhatsApp or email."), {
			status: 410,
			headers: { "Content-Type": "text/html" },
		});
	}

	const expected = await signCodToken(env.COD_LINK_SECRET, Number(orderId), exp);
	if (expected !== sig) {
		return new Response("Invalid signature", { status: 401 });
	}

	if (!env.SHOPIFY_ADMIN_TOKEN) {
		return new Response(simpleHtmlPage("This link isn't fully set up yet — please contact us instead."), {
			status: 503,
			headers: { "Content-Type": "text/html" },
		});
	}

	await tagOrder(env, Number(orderId), tag);
	return new Response(simpleHtmlPage(successMessage), { headers: { "Content-Type": "text/html" } });
}

async function tagOrder(env: Env, orderId: number, tag: string): Promise<void> {
	const res = await fetch(`https://${env.SHOPIFY_SHOP}/admin/api/${SHOPIFY_ADMIN_API_VERSION}/graphql.json`, {
		method: "POST",
		headers: {
			"X-Shopify-Access-Token": env.SHOPIFY_ADMIN_TOKEN!,
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			query: `mutation tagsAdd($id: ID!, $tags: [String!]!) {
				tagsAdd(id: $id, tags: $tags) { userErrors { field message } }
			}`,
			variables: { id: `gid://shopify/Order/${orderId}`, tags: [tag] },
		}),
	});

	if (!res.ok) {
		console.error("Shopify tagsAdd failed", res.status, await res.text());
	}
}

function codConfirmationEmailHtml(opts: { customerName: string; orderNumber: string; confirmUrl: string; cancelUrl: string }): string {
	const { customerName, orderNumber, confirmUrl, cancelUrl } = opts;
	return `
		<div style="font-family: Georgia, serif; max-width: 480px; margin: 0 auto; color: #2B241F;">
			<h1 style="font-size: 20px;">PEXX</h1>
			<p>Hi ${customerName},</p>
			<p>Thanks for your Cash on Delivery order <strong>${orderNumber}</strong>. Please confirm so we can pack and dispatch it.</p>
			<p style="margin: 24px 0;">
				<a href="${confirmUrl}" style="background: #9E3B2F; color: #fff; padding: 12px 20px; text-decoration: none; border-radius: 4px; margin-right: 12px;">Confirm my order</a>
				<a href="${cancelUrl}" style="color: #9E3B2F; text-decoration: underline;">Cancel order</a>
			</p>
			<p style="color: #666; font-size: 13px;">If we don't hear from you, we'll follow up before dispatch.</p>
		</div>
	`;
}

function simpleHtmlPage(message: string): string {
	return `<!doctype html><html><body style="font-family: Georgia, serif; text-align: center; padding: 60px 20px;"><p>${message}</p></body></html>`;
}

// --- PostHog server-side capture ---------------------------------------------------------

async function capturePosthog(env: Env, event: string, distinctId: string, properties: Record<string, unknown>): Promise<void> {
	if (!env.POSTHOG_PROJECT_KEY || !env.POSTHOG_HOST) return;

	try {
		const res = await fetch(`${env.POSTHOG_HOST}/i/v0/e/`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				api_key: env.POSTHOG_PROJECT_KEY,
				event,
				distinct_id: distinctId,
				properties,
				timestamp: new Date().toISOString(),
			}),
		});
		if (!res.ok) {
			console.error("PostHog capture failed", event, res.status, await res.text());
		}
	} catch (err) {
		// ponytail: analytics must never break the WhatsApp/COD send path — log and move on.
		console.error("PostHog capture threw", event, err);
	}
}
