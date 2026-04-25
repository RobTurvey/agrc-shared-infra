# Templates

This folder contains reusable bootstrap templates for AGRC repositories.

Initial templates included:
- `AGENTS.md.template`
- `Makefile.workteam.template`
- `.env.example.template`
- `.devcontainer/devcontainer.json.template`
- `.devcontainer/postCreate.sh.template`
- `.vscode/settings.json.template`
- `.vscode/mcp.json.template`

Usage:
1. Copy template into target repository.
2. Replace placeholders such as `<id>`, `<actor>`, and runtime defaults.
3. Validate with local project commands.

Notes:
- Keep MCP template servers placeholder-only in shared baseline.
- Define real MCP server commands/credentials in each target repository.
