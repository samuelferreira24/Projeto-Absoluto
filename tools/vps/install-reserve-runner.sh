#!/usr/bin/env bash
set -euo pipefail

: "${RUNNER_TOKEN:?Defina RUNNER_TOKEN com um token temporário de registro de runner do GitHub}"
REPO="${REPO:-https://github.com/samuelferreira24/Projeto-Absoluto}"
RUNNER_DIR="${RUNNER_DIR:-$HOME/actions-runner-reserve}"
LABEL="${LABEL:-abs-vps-01-reserve}"

mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR"

if [ ! -f .runner ]; then
  if [ ! -f actions-runner.tar.gz ]; then
    ARCH="$(uname -m)"
    case "$ARCH" in
      x86_64) PKG="actions-runner-linux-x64-2.329.0.tar.gz" ;;
      aarch64|arm64) PKG="actions-runner-linux-arm64-2.329.0.tar.gz" ;;
      *) echo "Arquitetura não suportada: $ARCH"; exit 1 ;;
    esac
    curl -fsSL -o actions-runner.tar.gz "https://github.com/actions/runner/releases/download/v2.329.0/$PKG"
  fi
  tar xzf actions-runner.tar.gz
  ./config.sh --unattended --url "$REPO" --token "$RUNNER_TOKEN" --name abs-vps-01-reserve --labels "$LABEL" --work _work --replace
fi

sudo ./svc.sh install absadmin || true
sudo ./svc.sh start
sudo ./svc.sh status
