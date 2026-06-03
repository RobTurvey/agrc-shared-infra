FROM mcr.microsoft.com/devcontainers/javascript-node:1-22-bookworm

ENV REPORTING_VENV=/opt/reporting-venv
ENV PATH="${REPORTING_VENV}/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      make jq golang-go ca-certificates curl awscli python3 python3-pip python3-venv bubblewrap \
    && python3 -m venv ${REPORTING_VENV} \
    && ${REPORTING_VENV}/bin/pip install --no-cache-dir --upgrade pip \
    && npm install -g playwright \
    && playwright install --with-deps chromium \
    && curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | bash \
    && (curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_NON_INTERACTIVE=1 CODEX_INSTALL_DIR=/usr/local/bin sh \
      || echo "WARNING: Codex CLI install failed during image build; postCreate will retry.") \
    && (curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash || npm install -g @beads/bd) \
    && command -v bd \
    && rm -rf /var/lib/apt/lists/*
