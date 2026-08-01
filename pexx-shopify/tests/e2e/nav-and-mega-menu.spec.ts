import { test, expect } from './helpers';

test.describe('Primary nav', () => {
  test('top-level links resolve to real pages', async ({ page, isMobile }) => {
    test.skip(isMobile, 'desktop-only header nav; mobile links live in the drawer, tested separately');
    await page.goto('/');
    const links: Record<string, string> = {
      Little: '/collections/little',
      Carry: '/collections/carry',
      Gifting: '/pages/gifting',
      Journal: '/blogs/news',
      About: '/pages/about',
    };
    for (const [label, expectedPath] of Object.entries(links)) {
      const link = page.getByRole('navigation', { name: 'Primary' }).getByRole('link', { name: label, exact: true });
      await expect(link).toHaveAttribute('href', expectedPath);
    }
  });

  test('legacy /collections/gifting redirects to the real hub, never renders blank', async ({ page }) => {
    const res = await page.goto('/collections/gifting');
    expect(new URL(page.url()).pathname).toBe('/pages/gifting');
    expect(res?.status()).toBeLessThan(400);
    // the old collection page had a heading + intro paragraph and nothing else —
    // assert the real hub's tiles are present, not just that *a* heading exists.
    // Scoped to <main>: the same link text also exists, hidden, in the mobile
    // drawer markup that's present in the DOM on every viewport.
    await expect(page.locator('main').locator('a', { hasText: /Kids|Weddings|Corporate|Festive/ }).first()).toBeVisible();
  });
});

test.describe('Desktop mega-menu', () => {
  test.skip(({ isMobile }) => isMobile, 'hover mega-menu is desktop-only; mobile uses the drawer, tested separately');

  for (const [parent, subcats] of Object.entries({
    Little: ['Quilts', 'Backpacks', 'Swaddles', 'Toiletry Pouches'],
    Carry: ['Backpacks', 'Toiletry Pouches'],
  })) {
    test(`${parent} mega-menu exposes its subcategory links`, async ({ page }) => {
      await page.goto('/');
      // Scoped to the header nav: "Little"/"Carry" also appear as a homepage
      // collection tile and a footer link, tripping strict mode otherwise.
      const trigger = page.getByRole('navigation', { name: 'Primary' }).getByRole('link', { name: parent, exact: true });
      await trigger.hover();
      // `[aria-expanded="true"]` alone also matches the predictive-search
      // dropdown elsewhere in the header — check the trigger's own state and
      // resolve its specific panel via aria-controls instead.
      await expect(trigger).toHaveAttribute('aria-expanded', 'true', { timeout: 3000 });
      const submenuId = await trigger.getAttribute('aria-controls');
      const panel = page.locator(`#${submenuId}`);
      await expect(panel).toBeVisible();
      for (const sub of subcats) {
        // Non-exact regex: each tile link's accessible name is the visible text
        // plus its <img alt="..."> (also the same word), which fails `exact`
        // matching even though only one real "Quilts" etc. exists on the page.
        await expect(page.getByRole('link', { name: new RegExp(sub, 'i') })).toBeVisible();
      }
    });
  }

  test('panel survives a realistic diagonal mouse move into it (hover-close regression)', async ({ page }) => {
    // Regression test for the mega-menu closing mid-hover on a natural mouse path.
    // Teleport-hover (page.hover()) does NOT reproduce this bug — Playwright jumps
    // the cursor directly to the target with no intermediate mousemove events, so a
    // gap-bridge bug in the panel's own event handling never gets exercised. This
    // walks a real multi-point path instead, same method that reproduced it live.
    await page.goto('/');
    const trigger = page.getByRole('navigation', { name: 'Primary' }).getByRole('link', { name: 'Little', exact: true });
    const triggerBox = await trigger.boundingBox();
    if (!triggerBox) throw new Error('nav trigger not found');

    await page.mouse.move(triggerBox.x + triggerBox.width / 2, triggerBox.y + triggerBox.height / 2, { steps: 10 });
    // `[aria-expanded="true"]` alone also matches the predictive-search
    // dropdown elsewhere in the header — check the trigger's own state and
    // resolve its specific panel via aria-controls instead.
    await expect(trigger).toHaveAttribute('aria-expanded', 'true', { timeout: 3000 });
    const submenuId = await trigger.getAttribute('aria-controls');
    const panel = page.locator(`#${submenuId}`);
    await expect(panel).toBeVisible();

    const panelBox = await panel.boundingBox();
    if (!panelBox) throw new Error('panel not found after opening');

    // Diagonal path from the trigger down into the panel, then across it toward a
    // subcategory link — the exact motion that used to close the panel mid-flight.
    const targetX = panelBox.x + panelBox.width * 0.4;
    const targetY = panelBox.y + panelBox.height * 0.5;
    await page.mouse.move(targetX, targetY, { steps: 25 });
    await expect(panel).toBeVisible();

    await expect(page.getByRole('link', { name: /Quilts/i })).toBeVisible();
  });
});

test.describe('Mobile nav drawer', () => {
  test.skip(({ isMobile }) => !isMobile, 'desktop uses hover mega-menu, tested separately');

  test('opening the drawer exposes the same subcategory structure as desktop', async ({ page }) => {
    await page.goto('/');
    // The hamburger trigger is a native <summary aria-label="Menu">, not a
    // <button> — Playwright doesn't compute an implicit "button" role for it,
    // so getByRole('button', ...) never matches. getByLabel works directly.
    await page.getByLabel('Menu', { exact: true }).click();
    const drawer = page.locator('.menu-drawer');
    // "Little"'s subcategory grid (Quilts/Backpacks/Swaddles/Toiletry Pouches)
    // renders inline under it as soon as the drawer opens — no expand click
    // needed; clicking the "Little" link itself would navigate away instead.
    await expect(drawer.getByRole('link', { name: /Quilts/i })).toBeVisible();
    await expect(drawer.getByRole('link', { name: /Backpacks/i })).toBeVisible();
    await expect(drawer.getByRole('link', { name: /Swaddles/i })).toBeVisible();
    await expect(drawer.getByRole('link', { name: /Toiletry Pouches/i })).toBeVisible();
  });
});
