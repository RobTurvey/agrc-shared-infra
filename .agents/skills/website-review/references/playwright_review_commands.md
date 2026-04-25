# Playwright Review Commands

## Baseline endpoint check
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4321/
```

## Install Playwright runtime (if missing)
```bash
npm install --save-dev playwright @playwright/test
npx playwright install chromium
```

## Run the AGRC baseline review script
```bash
node scripts/review/playwright_site_audit.mjs http://127.0.0.1:4321/
```

## Expected outputs
- JSON evidence under `artifacts/site-audit/<timestamp>/audit.json`
- Screenshots under `artifacts/site-audit/<timestamp>/screenshots/`
- Markdown report under `docs/reports/agrc-presale-site-audit-<timestamp>.md`

## Optional quick checks
```bash
npx playwright --version
node -v
npm -v
```

