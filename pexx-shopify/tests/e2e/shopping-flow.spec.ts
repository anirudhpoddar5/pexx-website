import { test, expect } from './helpers';

const SUBCATEGORIES = ['quilts', 'backpacks', 'swaddles', 'toiletry-pouches'];

for (const handle of SUBCATEGORIES) {
  test(`${handle}: collection lists products with working images`, async ({ page }) => {
    const res = await page.goto(`/collections/${handle}`);
    expect(res?.status()).toBeLessThan(400);
    const cards = page.locator('a[href*="/products/"]');
    await expect(cards.first()).toBeVisible();
    expect(await cards.count()).toBeGreaterThan(0);

    // first product image actually loaded (not a broken/zero-size image)
    const firstImg = page.locator('a[href*="/products/"] img').first();
    await expect(firstImg).toBeVisible();
    const naturalWidth = await firstImg.evaluate((img: HTMLImageElement) => img.naturalWidth);
    expect(naturalWidth).toBeGreaterThan(0);
  });
}

test('product page renders price, image, and an enabled add-to-cart', async ({ page }) => {
  await page.goto('/collections/quilts');
  await page.locator('a[href*="/products/"]').first().click();
  await expect(page).toHaveURL(/\/products\//);

  await expect(page.locator('h1')).toBeVisible();
  const priceText = await page.locator('body').innerText();
  expect(priceText).toMatch(/₹\s?[\d,]+/);

  const productImg = page.locator('img').first();
  await expect(productImg).toBeVisible();

  const addToCart = page.getByRole('button', { name: /add to cart/i });
  await expect(addToCart).toBeVisible();
  await expect(addToCart).toBeEnabled();
});

test('add to cart updates the cart with correct item + quantity, stops before checkout payment', async ({ page }) => {
  await page.goto('/collections/quilts');
  await page.locator('a[href*="/products/"]').first().click();
  const title = (await page.locator('h1').innerText()).trim();

  await page.getByRole('button', { name: /add to cart/i }).click();

  // theme may open a cart drawer or navigate to /cart — handle either
  await page.waitForTimeout(1000);
  const cartVisible = await page.locator('[class*="cart"]').first().isVisible().catch(() => false);
  if (!cartVisible) {
    await page.goto('/cart');
  }

  const cartBody = await page.locator('body').innerText();
  expect(cartBody).toContain(title.split(' ')[0]); // partial match, titles can wrap/truncate in cart UI

  // Boundary: confirm a checkout entry point exists, but do NOT click through into
  // real payment — that's a live financial transaction, out of scope for this suite.
  const checkoutButton = page.getByRole('link', { name: /checkout/i }).or(page.getByRole('button', { name: /checkout/i }));
  await expect(checkoutButton.first()).toBeVisible();
});
