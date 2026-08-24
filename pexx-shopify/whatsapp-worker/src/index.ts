interface Env {
	META_WA_TOKEN: string;
	SHOPIFY_WEBHOOK_SECRET: string;
	WA_PHONE_NUMBER_ID: string;
	WA_TEMPLATE_ORDER_CONFIRMED: string;
	WA_TEMPLATE_ORDER_DISPATCHED: string;
	WA_TEMPLATE_ORDER_DELIVERED: string;
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

		if (request.method === "GET" && (url.pathname === "/cod/confirm" || url.pathname === "/cod/cancel")) {
			return renderCodInterstitial(url);
		}
		if (request.method === "POST" && url.pathname === "/cod/apply") {
			return handleCodApply(request, env);
		}

		if (request.method !== "POST") {
			return new Response("Not found", { status: 404 });
		}

		if (
			url.pathname === "/webhooks/orders-create" ||
			url.pathname === "/webhooks/fulfillments-create" ||
			url.pathname === "/webhooks/fulfillments-update"
		) {
			const rawBody = await request.text();
			const validHmac = await verifyShopifyWebhook(request, rawBody, env.SHOPIFY_WEBHOOK_SECRET);
			if (!validHmac) {
				return new Response("Invalid signature", { status: 401 });
			}

			let payload: any;
			try {
				payload = JSON.parse(rawBody);
			} catch {
				// ponytail: malformed body should never happen from real Shopify webhooks, but throwing
				// here would 500 -> Shopify retries -> duplicate WhatsApp/COD sends. Fail soft instead.
				return new Response("Invalid JSON", { status: 400 });
			}

			if (url.pathname === "/webhooks/orders-create") return handleOrderCreated(payload, env, ctx);
			if (url.pathname === "/webhooks/fulfillments-create") return handleFulfillmentCreated(payload, env, ctx);
			return handleFulfillmentUpdated(payload, env, ctx);
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
		["verify"],
	);

	let signature: Uint8Array;
	try {
		signature = Uint8Array.from(atob(header), (c) => c.charCodeAt(0));
	} catch {
		return false;
	}

	// crypto.subtle.verify does a constant-time comparison internally.
	return crypto.subtle.verify("HMAC", key, signature, new TextEncoder().encode(rawBody));
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
		await sendCodConfirmationEmail(env, ctx, order);
	}

	return new Response("ok");
}

async function handleFulfillmentCreated(fulfillment: any, env: Env, ctx: ExecutionContext): Promise<Response> {
	const phone = extractPhone(fulfillment.destination?.phone);

	if (phone) {
		// fulfillment webhook has no customer name — look it up so the template can be personalized.
		const order = env.SHOPIFY_ADMIN_TOKEN ? await getOrderBasicInfo(env, fulfillment.order_id) : null;
		await sendTemplate(env, ctx, fulfillment, phone, env.WA_TEMPLATE_ORDER_DISPATCHED, [
			order?.firstName || "there",
			order?.orderName || `#${fulfillment.order_id}`,
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

	ctx.waitUntil(handleOrderDeliveredFollowUps(fulfillment, env, ctx));

	return new Response("ok");
}

// WhatsApp "delivered" send and the THANKYOU15 referral email are independent audiences
// (whoever has a phone on the shipment vs. whoever has an email and isn't already tagged),
// but both need the same order lookup — fetch it once and hand it to both.
async function handleOrderDeliveredFollowUps(fulfillment: any, env: Env, ctx: ExecutionContext): Promise<void> {
	const order = env.SHOPIFY_ADMIN_TOKEN ? await getOrderBasicInfo(env, fulfillment.order_id) : null;

	const phone = extractPhone(fulfillment.destination?.phone);
	if (phone) {
		await sendTemplate(env, ctx, fulfillment, phone, env.WA_TEMPLATE_ORDER_DELIVERED, [
			order?.firstName || "there",
			order?.orderName || `#${fulfillment.order_id}`,
		]);
	}

	await sendReferralThankYouEmail(env, fulfillment.order_id, order);
}

const REFERRAL_SENT_TAG = "thankyou15-sent";

async function sendReferralThankYouEmail(env: Env, orderId: number, order: OrderBasicInfo): Promise<void> {
	if (!env.RESEND_API_KEY || !env.RESEND_FROM || !env.SHOPIFY_ADMIN_TOKEN) {
		console.log("Referral thank-you email skipped — RESEND_API_KEY/RESEND_FROM/SHOPIFY_ADMIN_TOKEN not configured yet");
		return;
	}

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
		console.error("Referral thank-you email failed", res.status);
		await capturePosthog(env, "referral_email_failed", order!.email, { order_id: orderId, status: res.status });
		return;
	}

	const tagged = await tagOrder(env, orderId, REFERRAL_SENT_TAG);
	if (!tagged) {
		console.error("Referral email sent but failed to tag order — risk of a duplicate send later", orderId);
	}
}

type OrderBasicInfo = { email: string | null; firstName: string | null; orderName: string | null; tags: string[] } | null;

function shouldSendReferralEmail(order: OrderBasicInfo): order is NonNullable<OrderBasicInfo> & { email: string } {
	return Boolean(order?.email) && !order!.tags.includes(REFERRAL_SENT_TAG); // ponytail: dedupe against repeat "delivered" webhook fires
}

// Shared by the referral email, the delivered-WhatsApp send, and the shipped-WhatsApp send —
// all three just need "customer first name + order name" for a given order_id.
async function getOrderBasicInfo(env: Env, orderId: number): Promise<OrderBasicInfo> {
	const res = await fetch(`https://${env.SHOPIFY_SHOP}/admin/api/${SHOPIFY_ADMIN_API_VERSION}/graphql.json`, {
		method: "POST",
		headers: {
			"X-Shopify-Access-Token": env.SHOPIFY_ADMIN_TOKEN!,
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			query: `query getOrder($id: ID!) {
				order(id: $id) { name email customer { firstName } tags }
			}`,
			variables: { id: `gid://shopify/Order/${orderId}` },
		}),
	});

	if (!res.ok) {
		console.error("Shopify order lookup failed", res.status);
		return null;
	}

	const json: any = await res.json();
	if (json.errors) {
		console.error("Shopify order lookup returned errors", json.errors);
		return null;
	}

	const order = json.data?.order;
	if (!order) return null;
	return { email: order.email, firstName: order.customer?.firstName ?? null, orderName: order.name ?? null, tags: order.tags ?? [] };
}

function referralThankYouEmailHtml(opts: { customerName: string }): string {
	const customerName = escapeHtml(opts.customerName);
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
		let digits = raw.replace(/[^\d+]/g, "");
		if (digits.startsWith("+")) return digits;
		if (digits.startsWith("00")) digits = digits.slice(2); // international dialing prefix
		if (digits.length === 11 && digits.startsWith("0")) digits = digits.slice(1); // domestic trunk prefix (common in Indian checkout data)
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

	const distinctId = distinctIdFor(sourceRecord);

	if (!res.ok) {
		// ponytail: don't log the response body — Meta's error payload can echo the destination
		// phone number back, and this is a customer PII surface.
		console.error("WhatsApp send failed", res.status);
		ctx.waitUntil(capturePosthog(env, "whatsapp_send_failed", distinctId, { template: templateName, status: res.status }));
		return;
	}

	ctx.waitUntil(capturePosthog(env, "whatsapp_message_sent", distinctId, { template: templateName }));
}

function isCashOnDelivery(order: any): boolean {
	const names: string[] = order.payment_gateway_names || [];
	return names.some((name) => /cash on delivery|\bcod\b/i.test(name));
}

// --- COD email confirm/cancel -----------------------------------------------------------

async function sendCodConfirmationEmail(env: Env, ctx: ExecutionContext, order: any): Promise<void> {
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
		console.error("COD confirmation email failed", res.status);
		ctx.waitUntil(capturePosthog(env, "cod_email_failed", distinctIdFor(order), { order_id: order.id, status: res.status }));
	}
}

async function buildCodLink(env: Env, action: "confirm" | "cancel", orderId: number, exp: number): Promise<string> {
	const sig = await signCodToken(env.COD_LINK_SECRET!, action, orderId, exp);
	const params = new URLSearchParams({ order: String(orderId), exp: String(exp), sig });
	return `${env.WORKER_BASE_URL}/cod/${action}?${params.toString()}`;
}

async function importCodKey(secret: string, usage: "sign" | "verify"): Promise<CryptoKey> {
	return crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, [usage]);
}

async function signCodToken(secret: string, action: "confirm" | "cancel", orderId: number, exp: number): Promise<string> {
	const key = await importCodKey(secret, "sign");
	const payload = `${action}.${orderId}.${exp}`;
	const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(payload));
	return bufferToBase64Url(signature);
}

async function verifyCodToken(secret: string, action: string, orderId: number, exp: number, sig: string): Promise<boolean> {
	const key = await importCodKey(secret, "verify");
	const payload = `${action}.${orderId}.${exp}`;
	let signature: Uint8Array;
	try {
		signature = base64UrlToBuffer(sig);
	} catch {
		return false;
	}
	// crypto.subtle.verify does a constant-time comparison internally.
	return crypto.subtle.verify("HMAC", key, signature, new TextEncoder().encode(payload));
}

function bufferToBase64Url(buf: ArrayBuffer): string {
	const base64 = btoa(String.fromCharCode(...new Uint8Array(buf)));
	return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function base64UrlToBuffer(base64Url: string): Uint8Array {
	const padded = base64Url + "=".repeat((4 - (base64Url.length % 4)) % 4);
	const base64 = padded.replace(/-/g, "+").replace(/_/g, "/");
	return Uint8Array.from(atob(base64), (c) => c.charCodeAt(0));
}

const COD_ACTION_COPY: Record<"confirm" | "cancel", { verb: string; buttonLabel: string; success: string }> = {
	confirm: { verb: "confirm", buttonLabel: "Confirm order", success: "Thanks — your order is confirmed and on its way to dispatch." },
	cancel: { verb: "cancel", buttonLabel: "Cancel order", success: "Done — your order has been cancelled." },
};

// GET renders an interstitial only — no state change. Email security scanners and link-prefetchers
// (Gmail, Outlook, antivirus) fetch every URL in an email; if GET mutated the order they'd silently
// confirm and cancel it before the customer ever opened the message. Only the POST below can act.
function renderCodInterstitial(url: URL): Response {
	const action: "confirm" | "cancel" = url.pathname === "/cod/confirm" ? "confirm" : "cancel";
	const orderId = url.searchParams.get("order");
	const exp = url.searchParams.get("exp");
	const sig = url.searchParams.get("sig");

	if (!orderId || !exp || !sig) {
		return htmlResponse(simpleHtmlPage("Invalid link — please contact us."), 400);
	}
	if (Date.now() / 1000 > Number(exp)) {
		return htmlResponse(simpleHtmlPage("This link has expired. Please contact us on WhatsApp or email."), 410);
	}

	const { buttonLabel } = COD_ACTION_COPY[action];
	const html = `<!doctype html><html><body style="font-family: Georgia, serif; text-align: center; padding: 60px 20px;">
		<p>Tap below to ${action} order ${escapeHtml(orderId)}.</p>
		<form method="POST" action="/cod/apply">
			<input type="hidden" name="action" value="${action}">
			<input type="hidden" name="order" value="${escapeHtml(orderId)}">
			<input type="hidden" name="exp" value="${escapeHtml(exp)}">
			<input type="hidden" name="sig" value="${escapeHtml(sig)}">
			<button type="submit" style="background:#9E3B2F;color:#fff;border:none;padding:12px 28px;border-radius:4px;font-size:15px;">${buttonLabel}</button>
		</form>
	</body></html>`;
	return htmlResponse(html, 200);
}

async function handleCodApply(request: Request, env: Env): Promise<Response> {
	const form = await request.formData();
	const action = form.get("action");
	const orderId = form.get("order");
	const exp = Number(form.get("exp"));
	const sig = form.get("sig");

	if ((action !== "confirm" && action !== "cancel") || typeof orderId !== "string" || typeof sig !== "string" || !exp) {
		return htmlResponse(simpleHtmlPage("Invalid link — please contact us."), 400);
	}
	if (!env.COD_LINK_SECRET) {
		return htmlResponse(simpleHtmlPage("This link isn't fully set up yet — please contact us instead."), 503);
	}
	if (Date.now() / 1000 > exp) {
		return htmlResponse(simpleHtmlPage("This link has expired. Please contact us on WhatsApp or email."), 410);
	}

	const valid = await verifyCodToken(env.COD_LINK_SECRET, action, Number(orderId), exp, sig);
	if (!valid) {
		return htmlResponse(simpleHtmlPage("Invalid link — please contact us."), 401);
	}
	if (!env.SHOPIFY_ADMIN_TOKEN) {
		return htmlResponse(simpleHtmlPage("This link isn't fully set up yet — please contact us instead."), 503);
	}

	const tag = action === "confirm" ? "cod-confirmed" : "cod-cancelled";
	const tagged = await tagOrder(env, Number(orderId), tag);
	if (!tagged) {
		return htmlResponse(
			simpleHtmlPage("Something went wrong on our end and this wasn't recorded — please contact us on WhatsApp or email instead."),
			502,
		);
	}

	return htmlResponse(simpleHtmlPage(COD_ACTION_COPY[action].success), 200);
}

function htmlResponse(html: string, status: number): Response {
	return new Response(html, { status, headers: { "Content-Type": "text/html", "Cache-Control": "no-store" } });
}

async function tagOrder(env: Env, orderId: number, tag: string): Promise<boolean> {
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
		console.error("Shopify tagsAdd request failed", res.status);
		return false;
	}

	const json: any = await res.json();
	const userErrors = json.data?.tagsAdd?.userErrors ?? [];
	if (json.errors || userErrors.length > 0) {
		console.error("Shopify tagsAdd returned errors", json.errors ?? userErrors);
		return false;
	}
	return true;
}

function escapeHtml(value: string): string {
	const map: Record<string, string> = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
	return value.replace(/[&<>"']/g, (c) => map[c]);
}

function codConfirmationEmailHtml(opts: { customerName: string; orderNumber: string; confirmUrl: string; cancelUrl: string }): string {
	const customerName = escapeHtml(opts.customerName);
	const orderNumber = escapeHtml(opts.orderNumber);
	const { confirmUrl, cancelUrl } = opts;
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
			console.error("PostHog capture failed", event, res.status);
		}
	} catch (err) {
		// ponytail: analytics must never break the WhatsApp/COD send path — log and move on.
		console.error("PostHog capture threw", event, err);
	}
}
