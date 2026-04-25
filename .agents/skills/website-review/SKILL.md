---
name: website-review
description: Use this skill when the user asks to review, audit, or critique a website with evidence (for example marketing sites, landing pages, product pages, docs portals, or launch pages), and when the user expects Playwright-based browser validation plus a structured markdown report with severity and recommendations.
---

# website-review

## Purpose
Run a professional, repeatable website review workflow that produces evidence-first findings and prioritized recommendations.

## Invoke When
- User asks for a website review, quality audit, critique, or pre-launch assessment.
- User requests Playwright-based checks (rendering, DOM extraction, links, accessibility, mobile).
- User needs a structured markdown report with severity levels and remediation order.

## Do Not Invoke For
- Pure visual redesign/build requests without evaluation goals (use frontend implementation skills instead).
- Back-end API-only testing requests with no page-level UX/content checks.

## Inputs Expected
- Target URL(s)
- Scope constraints (single page vs crawl depth)
- Required evidence format (screenshots, JSON, markdown)
- Optional business context (conversion goals, audience, legal/regulatory constraints)

## Core Workflow
1. Confirm target URL is reachable.
2. Capture desktop rendering evidence and runtime health.
3. Extract DOM structure (title/meta/headings/CTAs/landmarks).
4. Check link integrity (internal + external with bounded retries/timeouts).
5. Run baseline accessibility heuristics (labels, alt text, heading hierarchy, lang, landmarks).
6. Run mobile viewport simulation and interaction risk checks (overflow, tap targets).
7. Produce structured markdown report using template in [`assets/website_review_report_template.md`](.agents/skills/website_review/assets/website_review_report_template.md:1).
8. Attach artifact paths and concise severity-ranked recommendations.

## Severity Model
Use this baseline mapping (customizable by project):
- **Critical**: blocks core journey, trust, or legal/compliance safety
- **High**: materially harms conversion/usability/accessibility
- **Medium**: meaningful quality issues with workaround available
- **Low**: polish/optimization improvements

## Deliverables
- Evidence artifacts (screenshots + machine-readable JSON)
- Structured markdown report
- Ordered remediation plan (top 3–5 next actions)

## Progressive Disclosure
- Rubric and check details: [`references/review_rubric.md`](.agents/skills/website_review/references/review_rubric.md:1)
- Playwright command patterns: [`references/playwright_review_commands.md`](.agents/skills/website_review/references/playwright_review_commands.md:1)
- Report template: [`assets/website_review_report_template.md`](.agents/skills/website-review/assets/website_review_report_template.md:1)
