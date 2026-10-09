#!/usr/bin/env bash
# Remove only regenerable package caches; preserve logs, backups, Docker rollback images,
# application data, runner workspaces, and every Ollama model tag.
set -uo pipefail
export HOME=/home/absadmin
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup="$HOME/abs-vps-inventory/cache-cleanup-$stamp"
mkdir -p "$backup"
log="$backup/cache-cleanup.log"
exec > >(tee -a "$log") 2>&1
echo "ABS_VPS_SAFE_CACHE_CLEANUP_BEGIN $stamp"
echo "=== PRECHECK ==="
df -h /
free -h
if pgrep -af '[n]pm (install|ci|update|uninstall|cache clean)|[n]pm exec' > "$backup/npm-processes.txt"; then
  echo "CACHE_CLEANUP_BLOCKED: npm operation appears active"
  cat "$backup/npm-processes.txt"
  exit 4
fi
before="$(df -B1 --output=avail / | tail -n 1 | tr -d ' ')"
for cache in /home/absadmin/.npm /root/.npm; do
  if sudo test -d "$cache"; then
    before_cache="$(sudo du -sb "$cache" 2>/dev/null | awk '{print $1}')"
    if command -v npm >/dev/null 2>&1; then
      if sudo npm cache clean --force --cache="$cache" >> "$log" 2>&1; then
        after_cache="$(sudo du -sb "$cache" 2>/dev/null | awk '{print $1}')"
        echo "NPM_CACHE_CLEAN_PASS path=$cache before_bytes=${before_cache:-unknown} after_bytes=${after_cache:-unknown}"
      else
        echo "NPM_CACHE_CLEAN_FAIL path=$cache"
      fi
    else
      echo "NPM_CACHE_CLEAN_SKIP path=$cache reason=npm_not_found"
    fi
  else
    echo "NPM_CACHE_CLEAN_SKIP path=$cache reason=path_absent"
  fi
done
if command -v apt-get >/dev/null 2>&1; then
  if sudo apt-get clean >> "$log" 2>&1; then
    echo "APT_CACHE_CLEAN_PASS"
  else
    echo "APT_CACHE_CLEAN_FAIL"
  fi
else
  echo "APT_CACHE_CLEAN_SKIP reason=apt_get_not_found"
fi
after="$(df -B1 --output=avail / | tail -n 1 | tr -d ' ')"
echo "PHYSICAL_BYTES_RECOVERED=$((after-before))"
echo "=== POSTCHECK ==="
df -h /
free -h
echo "PRESERVED: /var/log, /var/backups, $HOME/abs-local-ai-operation-backups, $HOME/abs-vps-inventory, Docker images/volumes, both runners, OpenClaw, ABS, Ollama, all remaining model tags"
echo "LOG=$log"
echo "ABS_VPS_SAFE_CACHE_CLEANUP_END"
