#!/data/data/com.termux/files/usr/bin/bash
set -eu

REPO_DIR="${ABS_REPO_DIR:-$HOME/Projeto-Absoluto}"
BIN_DIR="${PREFIX:-/data/data/com.termux/files/usr}/bin"

cat > "$BIN_DIR/abs-update" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -eu
REPO_DIR="${ABS_REPO_DIR:-$HOME/Projeto-Absoluto}"
cd "$REPO_DIR"
exec python -m abs_core.update_manager "$@"
EOF

chmod +x "$BIN_DIR/abs-update"

echo "ABS Update Manager installed."
echo
echo "Commands:"
echo "  abs-update status"
echo "  abs-update check"
echo "  abs-update apply"
echo "  abs-update rollback"
