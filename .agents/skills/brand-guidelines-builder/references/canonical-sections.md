# Canonical Sections Reference

Per-section markup, copy guidance, and pattern-notes format. Read the section relevant to what you're currently building.

## 01 / Voice

**What it is:** A short paragraph defining how the brand sounds in plain English, plus one example sentence rendered in the brand's actual H2 style.

**Why it comes first:** Tokens are downstream of voice. Putting voice at the top signals that the visual system serves the brand, not the other way around. Devs and designers landing on this page should know what kind of brand they're building for before they see a single colour.

**How to discover the voice:** Read 5–10 sentences from the prototype's hero copy, body text, and CTAs. Look for tone signals — formal / casual / confident / understated / playful / clinical. Then write 2–3 sentences capturing it in plain English. Avoid generic words like "professional" or "modern" — be specific. "Site-manager direct, not salesperson glossy" is good. "Modern and professional" is useless.

**Markup:**
```html
<section class="section" id="voice">
  <div class="section__inner">
    <div class="section__head">
      <div>
        <span class="section__num">01 / Voice</span>
        <h2 class="section__title">Brand essence</h2>
      </div>
      <p class="section__intro">
        Sixty years of industrial roof refurbishment, treated like a discipline. The voice is
        site-manager, not salesperson. Plain English, no jargon, the confidence of someone who
        has actually been on the roof.
      </p>
    </div>
    <p style="font-family: var(--font-display); font-size: clamp(1.4rem, 2.6vw, 2rem); text-transform: uppercase; line-height: 1.1;">
      Refurbish ageing industrial roofs without shutting down the site.
    </p>
  </div>
</section>
```

## 02 / Color

**What it is:** A swatch grid showing every colour token grouped by purpose.

**Grouping order:** neutrals (greys/blacks/whites) → brand (primary/teal/etc) → accent (safety colours, status colours). Within each group, darkest to lightest or most-prominent to least.

**Each swatch shows:** colour chip (the actual rendered colour), name (human-readable), hex + CSS variable name, "use for" note.

**Markup per swatch:**
```html
<div class="swatch">
  <div class="swatch__chip" style="background: #19a3a4;"></div>
  <div class="swatch__body">
    <span class="swatch__name">Teal</span>
    <span class="swatch__hex">#19A3A4 · --teal</span>
    <span class="swatch__use">Brand primary. CTAs, accent rules, icon defaults.</span>
  </div>
</div>
```

**Intro copy guidance:** Explain the palette philosophy in one sentence. "Steel neutrals carry the structure, teal carries the brand, safety orange reserved for kicker labels only."

## 03 / Type

**What it is:** Live specimens of every type style with the production font, plus the size / line-height / letter-spacing / weight values printed in monospace.

**Markup per row:**
```html
<div class="type-row">
  <span class="type-row__name">H2 / Section</span>
  <span style="font-family: 'Druk Wide Bold', sans-serif; font-size: clamp(2.4rem, 2.95vw, 2.6rem); font-weight: 700; text-transform: uppercase;">
    Refurbish ageing industrial roofs
  </span>
  <span class="type-row__values">
    clamp(2.4rem, 2.95vw, 2.6rem)<br>
    line 1.1 · tracking 0 · 700
  </span>
</div>
```

**Order of rows:** H1, H2, H3, H4, eyebrow, body, caption. Skip levels that don't exist in the prototype.

**Intro copy guidance:** State the font split. "Druk Wide Bold for display headlines. Space Grotesk for everything else: section H2s, card H3s, eyebrows, body, captions." Plus any rules — for example, "Druk Wide is ALWAYS uppercase."

## 04 / Spacing

**What it is:** Visual bars showing the spacing scale with token names and px values.

**Markup per row:**
```html
<div class="spacing-row">
  <span class="spacing-row__token">--space-1</span>
  <div class="spacing-row__bar" style="width: 4px;"></div>
  <span class="spacing-row__value">4px</span>
</div>
```

**Note:** The bar's `width` is inline so the visual matches the value. Bigger spacings = wider bars.

**Order:** smallest to largest.

**Intro copy guidance:** Explain the system. "Powers of 4 from 4 to 64, with a 96 + 128 for section spacing. Inline padding uses the lower half (4–16), block margins use the upper half (24–64)."

## 05 / Radii

**What it is:** Visual boxes showing each corner radius, named with their token.

**Markup:**
```html
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem;">
  <div style="border: 1px solid var(--line); border-radius: 4px; padding: 1.5rem;">
    <strong>Small</strong>
    <div style="font-family: monospace; font-size: 0.78rem; color: var(--text-soft); margin-top: 0.5rem;">
      4px · --radius-sm<br>Inputs, chips, list bullets.
    </div>
  </div>
  <!-- repeat for md, lg -->
</div>
```

**Intro copy guidance:** State the rule. "Three values. Inputs and small chips at 4px. Most components (cards, buttons, panels) at 6px. Larger surfaces (modals, hero CTA) at 8px. Nothing softer."

## 06 / Shadows

**What it is:** Sample cards showing each elevation level, with the box-shadow values.

**Markup:**
```html
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1.5rem;">
  <div style="padding: 1.5rem; border-radius: 6px; background: #fff; box-shadow: 0 12px 34px rgba(13, 19, 24, 0.06);">
    <span style="font-family: monospace; font-size: 0.75rem;">card · resting</span>
    <div style="font-family: monospace; font-size: 0.7rem; color: var(--text-soft); margin-top: 0.5rem;">
      0 12px 34px<br>rgba(13, 19, 24, 0.06)
    </div>
    <p style="font-size: 0.8rem; color: var(--text-soft); margin: 0.6rem 0 0;">
      All resting cards: project, info, service, accreditation, CTA band.
    </p>
  </div>
</div>
```

**Intro copy guidance:** Describe the elevation philosophy. "Soft, low-contrast, dark-warm. Used to lift cards above page surface and signal interactivity on hover. Never decorative. Always indicating depth."

## 06b / Iconography (skip if no icons)

**What it is:** Two parts — a colour reactivity demo (same icon on white vs on dark) proving `currentColor` works, then a grid of every icon labelled.

**Sprite handling:** Copy the prototype's `<svg><defs><symbol>...</symbol></defs></svg>` block verbatim into the top of `<body>` in brand.html. The `<use>` references in this section will resolve to those symbols.

**Markup (colour reactivity):**
```html
<div class="icon-color-demo">
  <div class="icon-color-demo__white">
    <svg class="icon" aria-hidden="true"><use href="#icon-roof"></use></svg>
    <span>on white</span>
  </div>
  <div class="icon-color-demo__dark">
    <svg class="icon" aria-hidden="true"><use href="#icon-roof"></use></svg>
    <span>on dark</span>
  </div>
</div>
```

The same icon renders teal on the white tile and white on the dark tile because `stroke="currentColor"` inherits the parent context. This is the most important demonstration on the page for devs — they'll see immediately that they don't have to manage colour variants per icon.

**Markup (icon grid):**
```html
<div class="icon-grid">
  <div class="icon-tile">
    <svg class="icon" aria-hidden="true"><use href="#icon-search"></use></svg>
    <span class="icon-tile__name">search</span>
  </div>
  <!-- one tile per icon -->
</div>
```

**Group order:** If there are both standard interface icons and custom domain icons (e.g. roofing-specific), use two grids with a small uppercase label between them ("Interface" / "Custom").

**Intro copy guidance:** State the technical contract. "Single-line set, 24x24 viewBox, 1.6 stroke, round joins. Every icon uses `stroke=\"currentColor\"`, so they inherit the parent's text colour. The same SVG renders teal on white and white on dark with no markup change."

## 07 / Layout

**What it is:** A breakpoint table showing every `@media` query the prototype uses, with what changes at each.

**Markup:**
```html
<table class="map-table">
  <thead>
    <tr><th>Breakpoint</th><th>Width</th><th>What changes</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><code>≤ 640px</code></td>
      <td>Mobile</td>
      <td>Single column. Hero h1 collapses to clamp(1.15rem, 5.3vw, 1.7rem). Mega menu becomes full-screen overlay. Top-bar phone collapses to icon-only.</td>
    </tr>
    <tr>
      <td><code>≤ 920px</code></td>
      <td>Tablet</td>
      <td>Footer reflows to three columns. Hero card stacks below hero copy.</td>
    </tr>
    <tr>
      <td><code>≤ 1180px</code></td>
      <td>Small desktop</td>
      <td>Hero CTA card moves under search bar. Mega menu detail panel narrows.</td>
    </tr>
  </tbody>
</table>
```

**Intro copy guidance:** Be honest about mobile-first vs desktop-first. "Mobile-first. The single biggest break is at 1180px, where the hero collapses from two columns to one and most card grids fall to two-up."

## 08 / Patterns

**What it is:** Live examples of every reusable composition in the prototype. This is the biggest section and the most important for dev handoff.

**Every pattern entry has THREE parts:**
1. `.pattern__label` — what it's called (in caps, monospace optional)
2. Live render — the working example using the prototype's actual classes
3. `.pattern__notes` block — spec values + a "use for:" guidance line, in monospace

**Markup template:**
```html
<div class="pattern">
  <span class="pattern__label">Buttons</span>
  <div style="display: flex; gap: 0.75rem;">
    <button class="button button--primary">Request a Survey</button>
    <button class="button button--ghost">Download brief</button>
  </div>
  <span class="pattern__notes">
    min-height 3.3rem · padding 0 1.35rem · radius 6px<br>
    font-weight 800 · tracking 0.03em · uppercase<br>
    use for: primary CTAs and secondary actions on light backgrounds
  </span>
</div>
```

**Patterns to include (if they exist in the prototype):**
- Buttons (both on light + dark backgrounds — two separate patterns)
- Eyebrow with glyph
- Section heading composition (eyebrow + H2 + lede)
- Info card (text-only)
- Image card (image-top)
- Arrow link / "view case study" style
- Numbered process list
- Callout / pull-quote
- Chips / metadata tags
- **Project-specific custom patterns** — anything the prototype invented that isn't a standard component. Document each one. Examples seen: aerial strip (full-bleed image with caption), marquee carousel (logo cycle), Q+A list (icons + bold answer), spotlight hover button, top-strip ticker.

**Critical:** Use the prototype's actual class names for the live render, not bespoke demo classes. The brand.html should look like the real site. Only fall back to `-demo` suffix classes when the production class needs isolation in the style guide context (icon-color-demo, spotlight-demo where you need a different background).

**Pattern notes format guidance:** Three short lines max. Spec values on the first line or two (`min-height · padding · radius · weight · tracking`), separated by middle dots. Then a `use for: <one-line guidance>` line. If the pattern has subtle technical notes (animation, mask, sprite reference), add them on a third line. Keep it tight. Devs scan, they don't read.

## 09 / Handoff

**What it is:** The translation table from the prototype's tokens to the production framework (almost always Tailwind). Plus a notes block at the end with anything else dev needs.

**Markup:**
```html
<table class="map-table">
  <thead>
    <tr>
      <th>Token</th>
      <th>Production value</th>
      <th>Tailwind equivalent</th>
      <th>Different from default?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>--teal</code></td>
      <td><code>#19A3A4</code></td>
      <td><code>cre.teal</code> in <code>tailwind.config.ts</code></td>
      <td>Yes. Add under <code>theme.extend.colors.cre</code>.</td>
    </tr>
    <tr>
      <td><code>--radius-md</code></td>
      <td><code>6px</code></td>
      <td><code>rounded-md</code></td>
      <td>No. Tailwind default is 6px.</td>
    </tr>
  </tbody>
</table>
```

**"Different from default?" column is required.** It saves dev hours. They need to know what to add to their config vs what works out of the box.

**Notes block after the table:** Anything that doesn't fit in the table. Common items:
- Font loading URLs (the actual woff or Google Fonts query string)
- `darkMode` config setting (usually `'class'` or unset)
- Required Tailwind plugins (`@tailwindcss/forms`, `@tailwindcss/typography`)
- Custom CSS layer needs (e.g. the spotlight hover requires a global pointermove listener)
- Any animations that need to be registered as Tailwind keyframes

**Intro copy guidance:** Explain the framing. "Every token in this system maps cleanly to a Tailwind config entry. Most align with Tailwind defaults. The list below covers what's different and what dev needs to add."
