// Render the portrait sequence (the TikTok cut) to PNG frame streams.
//
// Each beat in sequence/ is a self-contained 1080x1920 clip: a brand-colour
// wipe reveals it, its scene animation plays once and holds, then the wipe
// covers it again. We pause every animation and step a virtual clock across
// the 5400ms clip, so captures are frame-perfect and deterministic.
//
// Two passes are rendered from the same beats:
//   frames/sequence/        - with the hook captions
//   frames/sequence-clean/  - captions hidden, for a text-free export
//
// Beats are written back-to-back into one numbered stream per pass, so each
// beat's closing wipe meets the next beat's opening wipe as one continuous
// sweep. assemble-seq.mjs sets the playback frame rate.

import puppeteer from "puppeteer";
import { mkdir, rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = dirname(fileURLToPath(import.meta.url));

// One entry per file in sequence/, in play order. EDIT PER PROJECT.
const BEATS = ["example-beat.html"];

const W = 1080; // portrait 9:16, TikTok native
const H = 1920;
const CLIP_MS = 5400; // authored beat length (wipe duration in base-seq.css)
const PER = 162; // frames sampled per beat across the 5400ms timeline

// Two exports: one with the hook captions, one with them hidden.
const PASSES = [
  { dir: "sequence", hideCaptions: false },
  { dir: "sequence-clean", hideCaptions: true },
];

const browser = await puppeteer.launch({
  headless: true,
  args: ["--no-sandbox", "--hide-scrollbars", "--force-color-profile=srgb"],
});

for (const pass of PASSES) {
  const outDir = join(ROOT, "frames", pass.dir);
  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });

  let frame = 0;
  for (const beat of BEATS) {
    const page = await browser.newPage();
    await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
    await page.goto("file://" + join(ROOT, "sequence", beat), {
      waitUntil: "networkidle0",
    });
    if (pass.hideCaptions) {
      await page.addStyleTag({
        content: ".caption { display: none !important; }",
      });
    }
    await page.evaluate(() => document.fonts.ready);

    // Pause every animation so the virtual clock is the only thing moving time.
    await page.evaluate(() => {
      for (const a of document.getAnimations()) a.pause();
    });

    for (let i = 0; i < PER; i++) {
      const t = (i * CLIP_MS) / PER;
      await page.evaluate(async (time) => {
        for (const a of document.getAnimations()) a.currentTime = time;
        await new Promise((r) =>
          requestAnimationFrame(() => requestAnimationFrame(r)),
        );
      }, t);
      await page.screenshot({
        path: join(outDir, `${String(frame).padStart(4, "0")}.png`),
      });
      frame++;
    }

    await page.close();
    console.log(`captured ${pass.dir}/${beat}: ${PER} frames`);
  }
  console.log(`pass ${pass.dir}: ${frame} frames total`);
}

await browser.close();
console.log("sequence captured (captioned + clean)");
