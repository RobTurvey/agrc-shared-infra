---
name: brand-guidelines-builder
description: Build (or update) a single-file design system reference page — typically `brand.html` — from an existing HTML/CSS prototype. Use this skill whenever the user asks for "brand guidelines", a "design system page", a "style guide", a "tokens reference", a "brand.html", or wants to extract their colours / type scale / spacing / components into a shareable handoff artefact. Also trigger when the user mentions handing a prototype to a developer, porting design tokens to Tailwind, documenting their visual system, or producing a single-page reference of swatches + type specimens + component patterns. Even if the user only says "can you make me a style guide for this site" or "I need to give the dev a tokens page" — this is the skill. Works on any HTML/CSS prototype (vanilla, Vue, Nuxt, React); always produces a self-contained vanilla HTML output regardless of the source stack.
---

# Brand Guidelines Builder

You're being asked to extract a brand's visual system out of an existing HTML/CSS prototype and crystallise it into a single self-contained `brand.html` page. That page is the handoff artefact a developer will use to port the design into production. It must look like the brand, render every pattern live (no screenshots), and stay synced with the prototype whenever new patterns ship.

The goal: a developer with no prior context should be able to open `brand.html`, see every token + component the prototype uses, and know exactly what to build.

## When this skill triggers

The user is asking for a style guide / design system / tokens reference / brand.html / handoff page derived from a working prototype. Common phrasings:
- "make a brand guidelines page"
- "I need to give my dev a tokens reference"
- "build me a design system page from this prototype"
- "extract the colours / type / spacing into a single page"
- "this prototype needs a style guide"
- "document the visual system"

If the user already has a `brand.html` and asks you to add a new pattern to it, that's also this skill — follow the **Sync rule** below.

## What you're producing

A single file: `brand.html` in the same directory as the prototype (typically alongside `index.html`). One file, vanilla HTML + a local `<style>` block, no build step, no JS framework. The file embeds its own copy of any SVG sprite the prototype uses so it renders standalone. It is intentionally easy to email, version-control, or upload to a static host.

## Workflow

### 1. Locate the prototype

If the user hasn't pointed you at the files, scan the project for the main HTML (look for `index.html`, `home.html`, `*.html` in a `designs/`, `prototypes/`, or root folder) and its stylesheet (linked `<link rel="stylesheet">` or inline `<style>`). If multiple candidates, ask which is the source of truth before proceeding. Don't guess silently.

### 2. Extract the design tokens

Read the CSS and harvest:

- **Custom properties** at `:root` — colours, spacing, radii, shadows, max-widths, breakpoints
- **Font families** referenced in `font-family` declarations (especially heading vs body splits)
- **Type scale** — every `font-size` used on headings (h1/h2/h3/h4), eyebrows, body, captions, with the matching line-height and letter-spacing
- **Breakpoint media queries** — every `@media (max-width: ...)` or `@media (min-width: ...)`
- **Reusable components** — selectors like `.button`, `.card`, `.eyebrow`, `.info-card`, `.chip`, etc., plus any custom patterns the project has (carousels, marquees, hero compositions)

See `references/token-extraction.md` for grep patterns that find these quickly. **If the prototype has no `:root` tokens defined**, scan for repeated literal values (`#19a3a4` appearing 12 times → propose `--teal: #19a3a4`) and propose a token set in the brand.html with a note that these are derived, not declared.

### 3. Discover the voice

Brand voice is not in the CSS. Look at the prototype's hero copy, headings, body text, and CTA labels. Read 5–10 sentences. Is it formal? Casual? Confident? Site-manager-direct or salesperson-glossy? Write a short paragraph (2–3 sentences) summarising the voice in plain English, plus one example sentence in the brand's actual H2 style. This becomes section 01.

### 4. Build the page

Use `assets/brand.html.template` as the starting structure. The canonical section order is:

```
01 / Voice
02 / Color
03 / Type
04 / Spacing
05 / Radii
06 / Shadows
06b / Iconography      (skip if no icons in the prototype)
07 / Layout            (breakpoints + grid)
08 / Patterns          (live component examples)
09 / Handoff           (Tailwind translation table + porting notes)
```

For each section, follow `references/canonical-sections.md` which gives the exact markup, copy guidance, and notes-format for each one. The page must use the **prototype's actual CSS classes** for the demos wherever possible — not bespoke `-demo` classes — so it visually matches the production site. The exception is when an internal class needs isolation in the style guide context (e.g. the icon-color-demo on-white/on-dark tiles) — in those cases, use a `-demo` suffix.

### 5. Embed the icon sprite (if applicable)

If the prototype uses an SVG `<symbol>` sprite, copy the sprite block into the top of `<body>` in brand.html so the `<use>` references resolve. Then build a `06b / Iconography` section with two parts:
- A two-tile colour-reactivity demo: an on-white tile next to an on-dark tile, both rendering the same icon to prove `currentColor` works
- A grid of every icon labelled with its `#id`

### 6. Write the Tailwind translation table

Section 09 is the dev handoff bridge. For each CSS custom property, give the Tailwind config equivalent. Use this format:

| Token | Production | Tailwind equivalent | Different from default? |
|-------|------------|---------------------|------------------------|
| `--teal` | `#19a3a4` | `cre.teal` in `tailwind.config.ts` | Yes — new colour, add under `theme.extend.colors.cre` |
| `--radius-md` | `6px` | `rounded-md` | No — Tailwind default is 6px |

Always include the "Different from default?" column. Devs need to know what to add to their config vs what works out of the box. Also list anything else they need: font loading (the actual woff URLs), `darkMode` config (usually `'class'` or `false`), required Tailwind plugins, etc.

### 7. Sync rule (critical)

Once `brand.html` exists, treat it as the source of truth for the design system. Any time you ship a new pattern, animation, token, or component to `index.html` (or the prototype's main page), **update `brand.html` in the same turn**. Add a new entry to section 08, copy the live render, write the `pattern__notes` block, link any new icons in section 06b. If you don't sync, the dev will miss the pattern. Treat the prototype and brand.html as a single deliverable.

## Strong opinions encoded in this skill

These are not preferences. They're the rules that make this approach work. Follow them unless the user explicitly overrides.

1. **Single file.** `brand.html` is one self-contained `.html` — no build step, no framework, no external dependencies beyond the CDN images the prototype already uses. Vanilla HTML + a local `<style>` block + an embedded sprite if icons are used.

2. **Numbered sections with slash separators.** `01 / Voice`, `02 / Color`, etc. Never em-dashes. Em-dashes in copy are a known AI tell; they undermine credibility on a handoff document. Use commas, periods, colons, parentheses anywhere you'd reach for an em-dash. This applies to ALL copy in brand.html including pattern notes.

3. **Live demos beat screenshots.** Every pattern in section 08 must render in-browser using the actual CSS. If you can't render it, you can't ship it.

4. **Voice first.** Tokens are downstream of voice. Putting voice before colour signals that the visual system serves the brand, not the other way around.

5. **Use production classes.** The demos should use the prototype's real class names (`.button--primary`, `.info-card`, `.aerial-strip`, etc.). The brand.html should look like the real site, not a generic style guide template. Only use `-demo` suffixed classes when isolation is genuinely required (icon-color-demo, spotlight-demo).

6. **Pattern entries have three parts.** Label (what it's called), live render (the working example), and a monospace `pattern__notes` block with spec values + a "use for:" guidance line. All three. The notes are where dev context lives.

7. **Top strip header.** Brand.html opens with a thin top strip showing: brand name, version label (`v1 · Month YYYY`), source path (`designs/styles.css`), stack (`Nuxt 3 + Tailwind`, or whatever the production target is), and a button linking back to the homepage prototype. This grounds the artefact — anyone landing on the page knows what they're looking at and where it came from.

8. **Brand.html is the source of truth.** If a pattern lives in the prototype but not in brand.html, it's undocumented. The dev will miss it. Sync every time.

## Output format

When you're done, the user should have:

- A new file at `<prototype-dir>/brand.html` (or an updated existing one)
- Every section above filled in with the prototype's actual tokens and live patterns
- A top-strip header linking back to the prototype
- A Tailwind translation table in section 09 ready for the dev

Confirm with the user: "I've built brand.html at `<path>`. Open it next to the prototype to verify the patterns match. Want me to walk through any section, or are we good?"

## Files in this skill

- `SKILL.md` — these instructions
- `assets/brand.html.template` — starting skeleton with placeholder markers like `{{BRAND_NAME}}`, `{{TOKENS}}`, `{{ICON_SPRITE}}`. Read it once when you start, then fill it out
- `references/canonical-sections.md` — per-section markup, copy guidance, and pattern-notes format. Read this when building each section
- `references/token-extraction.md` — grep patterns and heuristics for harvesting tokens from any CSS file. Read at step 2 of the workflow
