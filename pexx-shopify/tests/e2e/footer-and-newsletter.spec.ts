import { test, expect } from './helpers';
// This one test needs the popup free to open, so it uses the raw Playwright
// test object instead of the popup-suppressing one everything else imports.
import { test as rawTest } from '@playwright/test';

const FOOTER_PAGES: Record<string, string> = {
  FAQ: '/pages/faq',
  'Contact Us': '/pages/contact',
  'Shipping Policy': '/pages/shipping-policy',
  'Returns & Refunds': '/pages/returns-refunds',
  'Our Story': '/pages/about',
  'Return Gifts': '/pages/return-gifts',
  'Gift to India': '/pages/gift-to-india',
};

for (const [label, path] of Object.entries(FOOTER_PAGES)) {
  test(`footer link "${label}" resolves`, async ({ page }) => {
    const res = await page.goto(path);
    expect(res?.status()).toBeLessThan(400);
    await expect(page.locator('h1')).toBeVisible();
  });
}

// There are TWO independent email/WhatsApp capture surfaces on the site — the
// footer newsletter form (#contact_form, tags "newsletter, footer") and a
// "Welcome offer" popup (#pexx-pop-form, tags "newsletter, popup"). Both share
// the same `contact[email]` field name, so any locator not scoped to one of
// them hits Playwright's strict-mode violation (found the hard way: the popup
// auto-opens on load, putting both forms in the DOM simultaneously).

test('footer newsletter form: email required, WhatsApp phone optional, consent checkbox drives the tag value', async ({ page }) => {
  await page.goto('/');
  const footerForm = page.locator('#contact_form');
  const emailInput = footerForm.locator('input[name="contact[email]"]');
  const phoneInput = footerForm.locator('input[name="contact[phone]"]');
  const tagsInput = footerForm.locator('input[name="contact[tags]"]');

  await expect(emailInput).toHaveAttribute('required', '');
  await expect(phoneInput).toBeVisible();
  await expect(phoneInput).not.toHaveAttribute('required', '');

  const baseTag = await tagsInput.inputValue();
  expect(baseTag).toContain('newsletter');
  expect(baseTag).not.toContain('whatsapp-optin');

  // Ticking WhatsApp consent should append whatsapp-optin to the hidden tag field —
  // this is what actually distinguishes "gave a number" from "consented to WhatsApp
  // messaging" in the resulting Shopify Customer record.
  await footerForm.getByLabel(/message me on WhatsApp/i).check();
  await expect(tagsInput).toHaveValue(/whatsapp-optin/);

  // NOTE: intentionally never submits. This form writes directly to Shopify's
  // Customer list with accepts_marketing=true — a real record on every test run.
});

rawTest('welcome popup: same capture pattern, tagged separately from the footer form', async ({ page }) => {
  await page.goto('/');
  const popup = page.getByRole('dialog', { name: 'Welcome offer' });
  await expect(popup).toBeVisible({ timeout: 5000 });

  const tagsInput = popup.locator('input[name="contact[tags]"]');
  await expect(tagsInput).toHaveValue(/newsletter, popup/);
  await expect(tagsInput).not.toHaveValue(/footer/); // confirms the two forms don't cross-tag

  // NOTE: intentionally never submits, same reason as the footer form test.
});
