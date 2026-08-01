import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: 1,
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: 'https://shop.poddarexp.com',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    // Pixel 7 (Chromium) rather than an iPhone preset (WebKit) — avoids a second
    // browser-engine download and matches PEXX's actual India-majority mobile
    // audience, which skews Android/Chrome.
    { name: 'mobile', use: { ...devices['Pixel 7'] } },
  ],
});
