// Assemble captured PNG frame sequences into looping promo GIFs.
//
// capture.mjs renders each scene as a square frame sequence. From that one
// square source this emits three delivery formats:
//   square    - 640x640,  social feed posts
//   portrait  - 720x1280 (9:16), stories and reels
//   landscape - 1280x720 (16:9), web and email banners
//
// Portrait and landscape are the square content scaled to fit one axis and
// padded on the other with the scene background colour. Every scene edge is
// already flat background, so the pad is seamless: the content reads as
// composed for the frame, not letterboxed.

import { execFile } from "node:child_process";
import { mkdir, readdir, stat } from "node:fs/promises";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const run = promisify(execFile);
const ROOT = dirname(fileURLToPath(import.meta.url));

const SCENES = ["example-scene"]; // must match capture.mjs
const FPS = 20; // must match capture.mjs
const BG = "0x0B0B0F"; // must match --bg in scenes/base.css

// content = the square edge length the scene is scaled to for each format.
const FORMATS = {
  square: { w: 640, h: 640, content: 640 },
  portrait: { w: 720, h: 1280, content: 720 },
  landscape: { w: 1280, h: 720, content: 720 },
};

// ffmpeg filtergraph: scale the square frames, pad to the target canvas
// centred with the bg colour, then generate a per-clip 256-colour palette and
// apply it with error-diffusion dithering (keeps gradients smooth in GIF).
function filterFor({ w, h, content }) {
  return (
    `[0:v]scale=${content}:${content}:flags=lanczos,` +
    `pad=${w}:${h}:(ow-iw)/2:(oh-ih)/2:${BG},split[a][b];` +
    `[a]palettegen=stats_mode=diff[p];` +
    `[b][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle`
  );
}

const outDir = join(ROOT, "out");
await mkdir(outDir, { recursive: true });

for (const scene of SCENES) {
  const framesDir = join(ROOT, "frames", scene);
  const frameCount = (await readdir(framesDir)).filter((f) =>
    f.endsWith(".png"),
  ).length;
  if (frameCount === 0) {
    throw new Error(`no frames in ${framesDir} - run "npm run render" first`);
  }
  for (const [name, fmt] of Object.entries(FORMATS)) {
    const out = join(outDir, `${scene}-${name}.gif`);
    await run("ffmpeg", [
      "-y",
      "-loglevel", "error",
      "-framerate", String(FPS),
      "-i", join(framesDir, "%03d.png"),
      "-filter_complex", filterFor(fmt),
      "-loop", "0",
      out,
    ]);
    const kb = Math.round((await stat(out)).size / 1024);
    console.log(`  ${scene}-${name}.gif  ${fmt.w}x${fmt.h}  ${kb} KB`);
  }
}
console.log("\nall GIFs assembled into out/");
