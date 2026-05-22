// Render each promo scene to a sequence of PNG frames.
//
// Every scene runs all of its CSS animations on one shared 4000ms infinite
// loop. We pause those animations, then step a virtual clock across the loop,
// screenshotting at each step. Seeking the Web Animations API like this gives
// frame-perfect, deterministic captures (no real-time jitter).
//
// Output: frames/<scene>/000.png ... Assemble into GIFs with assemble.mjs.

import puppeteer from "puppeteer";
import { mkdir, rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = dirname(fileURLToPath(import.meta.url));

// One entry per file in scenes/ (without the .html). EDIT PER PROJECT.
const SCENES = ["example-scene"];

const SIZE = 640; // CSS pixels - the square canvas
const SCALE = 2; // capture at 2x then downscale in ffmpeg for crisp edges
const LOOP_MS = 4000; // must match the animation duration used in the scenes
const FPS = 20;
const FRAMES = (LOOP_MS / 1000) * FPS;

const browser = await puppeteer.launch({
  headless: true,
  args: ["--no-sandbox", "--hide-scrollbars", "--force-color-profile=srgb"],
});

for (const scene of SCENES) {
  const page = await browser.newPage();
  await page.setViewport({ width: SIZE, height: SIZE, deviceScaleFactor: SCALE });
  await page.goto("file://" + join(ROOT, "scenes", `${scene}.html`), {
    waitUntil: "networkidle0",
  });
  await page.evaluate(() => document.fonts.ready);

  const outDir = join(ROOT, "frames", scene);
  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });

  // Pause every animation so the virtual clock is the only thing moving time.
  await page.evaluate(() => {
    for (const a of document.getAnimations()) a.pause();
  });

  for (let i = 0; i < FRAMES; i++) {
    const t = (i * LOOP_MS) / FRAMES;
    await page.evaluate(async (time) => {
      for (const a of document.getAnimations()) a.currentTime = time;
      // Wait for the new computed styles to paint before the screenshot.
      await new Promise((r) =>
        requestAnimationFrame(() => requestAnimationFrame(r)),
      );
    }, t);
    await page.screenshot({
      path: join(outDir, `${String(i).padStart(3, "0")}.png`),
    });
  }

  await page.close();
  console.log(`captured ${scene}: ${FRAMES} frames`);
}

await browser.close();
console.log("all scenes captured");
