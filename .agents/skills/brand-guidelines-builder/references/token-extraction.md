# Token Extraction Reference

Grep patterns and heuristics for harvesting design tokens from any CSS file. Use these at step 2 of the workflow.

## Custom properties at :root

The most reliable source. Get them in one pass:

```bash
grep -nE "^\s*--[a-z0-9-]+:" path/to/styles.css | head -100
```

Or to scope to the `:root` block specifically:

```bash
awk '/:root/,/}/' path/to/styles.css | grep -E "--[a-z]"
```

**Typical token namespaces to expect:**
- `--color-*`, `--brand-*`, or named colours (`--teal`, `--steel-950`)
- `--space-*`, `--gap-*`
- `--radius-*`
- `--shadow-*`
- `--font-*` (for stack names if defined as variables)
- `--max-*` or `--container-*`
- `--breakpoint-*` (less common in CSS, more in JS)

## Font families

```bash
grep -nE "font-family\s*:" path/to/styles.css | sort -u | head -20
```

Look for two distinct stacks in most projects: a display face for headings and a body face for everything else. Note any explicit text-transform rules paired with the display face — they're brand rules, not just styling (e.g. Druk Wide is always uppercase).

## Type scale

Find every `font-size` and its context:

```bash
grep -nB1 -A3 "font-size" path/to/styles.css | grep -E "^[^-]" | head -60
```

For each heading level, harvest:
- `font-size` (note `clamp()` usage — that's responsive typography)
- `line-height`
- `letter-spacing`
- `font-weight`
- `text-transform` (uppercase rules)

Build a table of: H1, H2, H3, H4, eyebrow, body, lede, caption. Each row gets a `font-size / line-height / letter-spacing / weight` quartet.

## Breakpoints

```bash
grep -nE "@media\s*\([^)]+\)" path/to/styles.css | sort -u | head
```

Common values: 640, 720, 768, 920, 1024, 1180, 1200, 1280. Use the actual values the prototype uses — don't invent.

For each breakpoint, the brand.html layout section needs a "what changes" summary. Either grep the rules inside that media query, or just describe the obvious layout shifts (single column, card grid drops, hero stacks).

## Component selectors

Find reusable patterns:

```bash
grep -nE "^\.[a-z][a-z0-9-]*\s*\{" path/to/styles.css | head -50
```

Then for the candidates that look reusable (button, card, eyebrow, chip, etc.), check the HTML to confirm they're actually used:

```bash
grep -c "class=\"[^\"]*\.button" path/to/index.html
```

## When the prototype has NO :root tokens

Some prototypes use literal values everywhere (`color: #19a3a4`) instead of variables. In that case, scan for repeated literals:

```bash
grep -oE "#[0-9a-f]{3,6}" path/to/styles.css | sort | uniq -c | sort -rn | head -20
```

Anything appearing 4+ times is a candidate token. Propose names based on context:
- Most-used dark colour → text or steel
- Most-used brand-adjacent colour → primary or accent
- Greys → neutral-100/200/300 etc

Add a note in brand.html section 02 that these tokens are "derived from observed values" so the dev knows to formalise them.

Same approach for spacing — `padding: 24px` appearing repeatedly suggests `--space-6: 24px` (using a 4-multiplier scale).

## SVG icon sprite

If the prototype uses an inline SVG sprite:

```bash
grep -n "<symbol" path/to/index.html | head -20
```

Each `<symbol id="...">` is an icon. Note the `id` (these are the names you'll list in the icon section), and the contents (so you can copy the full sprite block into brand.html).

If the sprite is referenced externally (e.g. `<use href="/icons.svg#search">`), grab the file:

```bash
grep -E "<symbol|href=" path/to/icons.svg | head
```

## Heuristics

- **A "token" is anything used more than 3 times.** One-off literals are styling, not tokens.
- **Component classes follow BEM-ish naming.** `.block`, `.block__element`, `.block--modifier`. If you see this pattern, that block is reusable.
- **Inline `style=""` attributes hide tokens.** Grep the HTML too: `grep -oE 'style="[^"]*"' index.html | grep -oE "#[0-9a-f]+" | sort | uniq -c`
- **Anything inside a media query is probably responsive overrides, not new tokens.** Don't dedupe tokens by media query.
- **Comments in CSS often reveal intent.** `/* Brand teal */`, `/* Soft elevation */` — preserve the author's naming when extracting.

## When done

You should have, in your working memory:
- A list of all CSS custom properties with their values
- The font stack(s) used
- The full type scale with all four properties per row
- Every breakpoint
- A list of reusable component class names
- The SVG sprite (if any) with all icon IDs

Now you can fill in the template.
