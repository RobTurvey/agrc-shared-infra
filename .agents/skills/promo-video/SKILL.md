---
name: promo-video
description: Build social promo assets for a brand or product - looping GIFs in square/portrait/landscape, plus a captioned, music-synced portrait video for TikTok, Reels and Shorts. Trigger whenever the user wants a promo video, animated ad, sizzle reel, launch teaser, demo video, social media GIFs, or "a video for [product]". Scenes are hand-built HTML/CSS animations rendered to frames with Puppeteer and assembled with ffmpeg; the skill bundles a ready-to-copy pipeline (capture + assemble scripts, base CSS, example scene and beat). Use when creating or updating motion promo content for any brand, app or software.
---

# Promo video and GIF builder

This skill builds, from hand-authored HTML/CSS animation scenes:

- **Looping GIFs** of each scene in 3 aspect ratios: square 1:1, portrait 9:16, landscape 16:9.
- **A portrait sequence video** (MP4) that chains the scenes with brand-colour wipe transitions, hook captions, and a soundtrack matched to the video length. It exports a captioned version and a clean (no-text) version.

Everything is deterministic: each scene's CSS animations run on one shared loop; the renderer pauses them and steps a virtual clock, screenshotting each frame. No real-time jitter.

The scenes are designed motion graphics (animated UI mockups, feature callouts, headline reels), not screen recordings.

## Prerequisites

- Node.js, and `ffmpeg` + `ffprobe` on PATH (check with `ffmpeg -version`).
- The pipeline kit is in `template/` next to this file.

## Setting up for a new project

1. Copy the kit into the project as a `promo/` folder:
   `cp -R <this-skill-dir>/template <project>/promo`
2. `cd <project>/promo && npm install` (installs Puppeteer; first run also downloads Chromium).
3. Gather from the user: the **brand palette** (hex values), a **logo** (SVG preferred), and for the video a **music track** (mp3). Ask if not supplied. If only a logo or site is given, pull the colours from there.
4. Replace `assets/logo.svg` with the real logo. Put the track at `assets/track.mp3`.
5. Set the brand palette in the `:root` block of BOTH `scenes/base.css` and `sequence/base-seq.css`. Use the same values in each. Also update the radial-glow `rgba(...)` in each `.stage` rule and `BG` in `assemble.mjs` (must equal `--bg`).
6. Pick an output name: set `PREFIX` in `assemble-seq.mjs`.

## The two pipelines

### GIFs - `npm run build`

- `capture.mjs` renders each scene in `scenes/` to `frames/<scene>/`.
- `assemble.mjs` turns each scene's frames into 3 GIFs (square, portrait, landscape) in `out/`. Portrait and landscape are the square content scaled and padded with the background colour. This is seamless ONLY because every scene keeps flat background at its four edges.
- Per project: edit the `SCENES` array in both `capture.mjs` and `assemble.mjs`.

### Sequence video - `npm run build-seq`

- `capture-seq.mjs` renders each beat in `sequence/` twice: once with hook captions, once with them hidden. Output: `frames/sequence/` and `frames/sequence-clean/`.
- `assemble-seq.mjs` encodes both to MP4 in `out/`, muxes `assets/track.mp3`, and sets the frame rate so the video length exactly equals the track. With no track it exports silent at 30fps.
- Per project: edit the `BEATS` array in `capture-seq.mjs`.

## Authoring a scene - `scenes/<name>.html`

Copy `scenes/example-scene.html`. Rules:

- One `.stage` (square). Link `base.css`.
- Every CSS animation runs on the SAME `4000ms linear infinite` loop. Stagger reveals with keyframe percentages, never `animation-delay`.
- Keep content centred so all four edges stay flat background; this is what makes the portrait/landscape pad seamless.
- End the scene with `<div class="flash"></div>`: the brand-colour overlay that is opaque at the loop boundary and hides the seam so the GIF loops cleanly.
- The final keyframe state should look good; in the sequence video it doubles as a hold frame.

## Authoring a sequence beat - `sequence/<name>.html`

Copy `sequence/example-beat.html`. Each beat is a one-shot 5400ms clip:

- Link `base-seq.css`. Portrait `.stage` (1080x1920).
- Beat animations play ONCE: `<name> 4000ms linear 350ms 1 both`. The 350ms delay lets the opening wipe clear first; `both` holds the end state through the hold.
- To reuse a square scene's component, paste its component CSS, wrap the markup in a `.group`, and `transform: scale(N)` it up to fill the portrait frame. The layout box is unscaled so flex centring still works; tune `N` with a smoke frame.
- Add `<div class="caption"><span>HOOK LINE</span></div>` for the on-screen text.
- End with `<div class="wipe"></div>`. Every beat starts and ends fully covered by the wipe, so consecutive beats concatenate into one continuous sweep.

## Key techniques

- **Deterministic capture**: pause every animation, set `currentTime`, wait two `requestAnimationFrame`s, then screenshot. Capture at 2x and downscale for crisp edges.
- **Loop seam / beat join**: `.flash` (GIFs) and `.wipe` (video) are opaque brand colour at clip boundaries. The flash hides a loop seam; the wipe, opaque at both ends of every beat, joins beats into one sweep.
- **Seamless pad**: portrait/landscape GIFs are the square scaled and padded with `--bg`. Works only because scene edges are flat background.
- **Audio match**: render a fixed frame count, then set output fps = frameCount / audioDuration so the video lands exactly on the track. Mux the mp3 as AAC.
- **With / without captions**: render the sequence twice; the clean pass injects `.caption { display: none }`.

## Gotchas

- Smoke-test ONE frame per scene or beat before a full render. Render it, view it, fix layout, then commit to the full render. Saves minutes per mistake.
- Absolutely-positioned text inside a narrow container can wrap unexpectedly. Use `white-space: nowrap` or an explicit width.
- GIF file size scales with how much of the frame moves. A full-screen sweep or a spinning element produces large files; that is expected.
- `ffmpeg` GIF quality: keep `palettegen=stats_mode=diff` + `paletteuse=dither=sierra2_4a` to stop gradients banding.
- Always confirm the brand palette with the user before rendering. Never guess a brand's colours.
