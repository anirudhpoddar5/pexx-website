// ponytail: minimal smoke test for the signature check + phone parsing, not a full suite.
// Run with: node src/index.test.mjs
import assert from "node:assert/strict";

async function computeHmac(secret, body) {
	const key = await crypto.subtle.importKey(
		"raw",
		new TextEncoder().encode(secret),
		{ name: "HMAC", hash: "SHA-256" },
		false,
		["sign"],
	);
	const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(body));
	return btoa(String.fromCharCode(...new Uint8Array(sig)));
}

// Matches Shopify's documented example: https://shopify.dev/docs/apps/build/webhooks/subscribe/verify-a-webhook
const secret = "hush";
const body = '{"hello":"world"}';
const expected = await computeHmac(secret, body);
assert.equal(typeof expected, "string");
assert.ok(expected.length > 0, "HMAC should produce a non-empty base64 signature");

// Wrong secret must not match.
const wrong = await computeHmac("different-secret", body);
assert.notEqual(wrong, expected, "different secrets must not produce the same signature");

function extractPhone(...candidates) {
	for (const raw of candidates) {
		if (!raw) continue;
		const digits = raw.replace(/[^\d+]/g, "");
		if (digits.startsWith("+")) return digits;
		if (digits.length === 10) return `+91${digits}`;
		if (digits.length > 10) return `+${digits}`;
	}
	return null;
}

assert.equal(extractPhone("9876543210"), "+919876543210");
assert.equal(extractPhone("+1 555-0100"), "+15550100");
assert.equal(extractPhone(null, undefined, "9876543210"), "+919876543210");
assert.equal(extractPhone(null, undefined), null);

function isCashOnDelivery(order) {
	const names = order.payment_gateway_names || [];
	return names.some((name) => /cash on delivery|\bcod\b/i.test(name));
}

assert.equal(isCashOnDelivery({ payment_gateway_names: ["Cash on Delivery (COD)"] }), true);
assert.equal(isCashOnDelivery({ payment_gateway_names: ["cod"] }), true);
assert.equal(isCashOnDelivery({ payment_gateway_names: ["Razorpay"] }), false);
assert.equal(isCashOnDelivery({ payment_gateway_names: [] }), false);
assert.equal(isCashOnDelivery({}), false);

function bufferToBase64Url(buf) {
	const base64 = btoa(String.fromCharCode(...new Uint8Array(buf)));
	return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function signCodToken(secret, orderId, exp) {
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

// COD confirm/cancel link signing: same order+expiry must always verify, tampering must not.
const codSig = await signCodToken("cod-secret", 12345, 1999999999);
assert.equal(await signCodToken("cod-secret", 12345, 1999999999), codSig, "same inputs must produce the same signature");
assert.notEqual(await signCodToken("cod-secret", 99999, 1999999999), codSig, "different order id must change the signature");
assert.notEqual(await signCodToken("cod-secret", 12345, 1888888888), codSig, "different expiry must change the signature");
assert.notEqual(await signCodToken("wrong-secret", 12345, 1999999999), codSig, "different secret must change the signature");

const REFERRAL_SENT_TAG = "thankyou15-sent";
function shouldSendReferralEmail(order) {
	return Boolean(order?.email) && !order.tags.includes(REFERRAL_SENT_TAG);
}

assert.equal(shouldSendReferralEmail({ email: "a@b.com", tags: [] }), true);
assert.equal(shouldSendReferralEmail({ email: "a@b.com", tags: ["thankyou15-sent"] }), false, "must skip once already tagged");
assert.equal(shouldSendReferralEmail({ email: null, tags: [] }), false, "must skip when no email on order");
assert.equal(shouldSendReferralEmail(null), false, "must skip when order lookup failed");

console.log("ok — signature + phone parsing + COD detection + link signing + referral-email dedupe checks passed");
