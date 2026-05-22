// Assemble the captured portrait frame streams into the sequence MP4s, with
// the soundtrack muxed in and the video length matched to the audio.
//
//   out/<PREFIX>-tiktok.mp4        - captioned
//   out/<PREFIX>-tiktok-clean.mp4  - no captions
//
// The beats are rendered as a fixed number of frames; the playback frame rate
// is derived from the audio duration, so the whole sequence lands exactly on
// the track (assets/track.mp3). With no track present it exports silent at
// 30fps. H.264 + yuv420p + faststart plays everywhere; the mp3 is muxed AAC.

import { execFile } from "node:child_process";
import { mkdir, readdir, stat, access } from "node:fs/promises";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const run = promisify(execFile);
const ROOT = dirname(fileURLToPath(import.meta.url));

const PREFIX = "promo"; // output filename prefix - SET PER PROJECT
const AUDIO = join(ROOT, "assets", "track.mp3");

async function probeDuration(file) {
  const { stdout } = await run("ffprobe", [
    "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=nw=1:nk=1",
    file,
  ]);
  const d = parseFloat(stdout.trim());
  if (!Number.isFinite(d)) throw new Error(`could not read duration of ${file}`);
  return d;
}

let audioDur = null;
try {
  await access(AUDIO);
  audioDur = await probeDuration(AUDIO);
} catch {
  console.log("no assets/track.mp3 found - exporting silent at 30fps");
}

const outDir = join(ROOT, "out");
await mkdir(outDir, { recursive: true });

const VARIANTS = [
  { frames: "sequence", out: `${PREFIX}-tiktok.mp4`, label: "captioned" },
  { frames: "sequence-clean", out: `${PREFIX}-tiktok-clean.mp4`, label: "no captions" },
];

for (const v of VARIANTS) {
  const framesDir = join(ROOT, "frames", v.frames);
  const count = (await readdir(framesDir)).filter((f) =>
    f.endsWith(".png"),
  ).length;
  if (count === 0) {
    throw new Error(`no frames in ${framesDir} - run "npm run render-seq" first`);
  }

  // Frame rate that makes the full clip land exactly on the audio length.
  const fps = audioDur ? (count / audioDur).toFixed(4) : "30";
  const out = join(outDir, v.out);

  const args = ["-y", "-loglevel", "error", "-framerate", fps];
  args.push("-i", join(framesDir, "%04d.png"));
  if (audioDur) args.push("-i", AUDIO);
  args.push(
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-profile:v", "high",
    "-crf", "18",
  );
  if (audioDur) args.push("-c:a", "aac", "-b:a", "192k", "-shortest");
  args.push("-movflags", "+faststart", out);

  await run("ffmpeg", args);

  const mb = ((await stat(out)).size / 1048576).toFixed(1);
  const secs = audioDur ? audioDur.toFixed(1) : (count / 30).toFixed(1);
  console.log(`assembled ${v.out}  (${v.label})  ${count} frames @ ${fps}fps  ${secs}s  ${mb} MB`);
}

console.log("\ndone - both MP4s in out/");
