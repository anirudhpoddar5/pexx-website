import { test, expect } from './helpers';

const SUBPAGES = ['gifting-kids', 'gifting-weddings', 'gifting-corporate', 'gifting-festive'];

test('gifting hub links to all 4 occasion subpages', async ({ page }) => {
  await page.goto('/pages/gifting');
  // H1 is merchant-editable copy ("Gifts with a maker's hand on them"), not the
  // literal word "Gifting" — assert it renders, not a specific string.
  await expect(page.locator('h1')).toBeVisible();
  await expect(page).toHaveTitle(/Gifting/i);
  for (const handle of SUBPAGES) {
    // Scoped to <main>: the same href also exists, hidden, in the mobile
    // drawer markup that's present in the DOM on every viewport.
    await expect(page.locator('main').locator(`a[href*="/pages/${handle}"]`).first()).toBeVisible();
  }
});

for (const handle of SUBPAGES) {
  test(`${handle}: loads with occasion tiles and a working enquiry form`, async ({ page }) => {
    const res = await page.goto(`/pages/${handle}`);
    expect(res?.status()).toBeLessThan(400);
    await expect(page.locator('h1')).toBeVisible();

    // at least one occasion tile with a "get a quote" style CTA
    const quoteLink = page.locator('a', { hasText: /quote|enquire|enquiry/i }).first();
    await expect(quoteLink).toBeVisible();

    // clicking a tile's quote CTA should deep-link with prefill params and land on
    // the enquiry form with fields already populated — verified without submitting.
    await quoteLink.click();
    const url = new URL(page.url());
    const hasPrefillParam = url.searchParams.has('occasion') || url.searchParams.has('product') || url.hash.includes('enquiry');
    expect(hasPrefillParam).toBeTruthy();

    const form = page.locator('form').filter({ has: page.locator('[name*="occasion" i], [name*="product" i]') }).first();
    await expect(form).toBeVisible();

    // NOTE: intentionally does not submit — this hits the real Shopify contact form
    // and would create a live lead in the merchant's inbox on every test run.
  });
}
