#!/data/data/com.termux/files/usr/bin/bash
set -eu

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="${ABS_REPO_DIR:-$HOME/Projeto-Absoluto}"
SERVICE_DIR="$PREFIX/var/service/abs-gateway"

mkdir -p "$SERVICE_DIR/log"

cat > "$SERVICE_DIR/run" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -eu
REPO_DIR="${ABS_REPO_DIR:-$HOME/Projeto-Absoluto}"
export ABS_REPO_DIR="$REPO_DIR"
export ABS_LOCAL_AI_URL="${ABS_LOCAL_AI_URL:-http://127.0.0.1:8080}"
export ABS_OPENAI_COMPAT_HOST="${ABS_OPENAI_COMPAT_HOST:-127.0.0.1}"
export ABS_OPENAI_COMPAT_PORT="${ABS_OPENAI_COMPAT_PORT:-8788}"
cd "$REPO_DIR"
exec python -m abs_core.openai_compat
EOF

cat > "$SERVICE_DIR/log/run" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -eu
mkdir -p "$HOME/.abs/log/gateway"
exec svlogd "$HOME/.abs/log/gateway"
EOF

chmod +x "$SERVICE_DIR/run" "$SERVICE_DIR/log/run"

if command -v sv-enable >/dev/null 2>&1; then
  sv-enable abs-gateway || true
fi
if command -v sv >/dev/null 2>&1; then
  sv up abs-gateway || true
fi

echo "ABS gateway service installed at: $SERVICE_DIR"
echo "Endpoint: http://127.0.0.1:8788/v1"
echo "Local AI: ${ABS_LOCAL_AI_URL:-http://127.0.0.1:8080}"
