#!/usr/bin/env bash
# Controlled six-model ABS operation. Fixed model allowlist; never accepts shell input.
set -uo pipefail
export HOME=/home/absadmin
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
cd "$HOME/Projeto-Absoluto" || exit 2
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup="$HOME/abs-local-ai-operation-backups/$stamp"
mkdir -p "$backup"
log="$backup/operation.log"
exec > >(tee -a "$log") 2>&1

echo "ABS_LOCAL_AI_FULL_OPERATION_BEGIN $stamp"
echo "=== BASELINE ==="
hostname
date -Is
free -h
df -h /
curl -fsS --max-time 10 http://127.0.0.1:8787/health || true
curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags > "$backup/ollama-tags-before.json" || { echo "BLOCKED: Ollama API unavailable"; exit 3; }
ollama list | tee "$backup/ollama-list-before.txt"
curl -fsS --max-time 5 http://127.0.0.1:11434/api/ps | tee "$backup/ollama-ps-before.json" || true
sudo systemctl cat abs.service > "$backup/abs-service.before.txt" 2>&1 || true
sudo systemctl show abs.service -p Environment -p EnvironmentFiles > "$backup/abs-service-env.before.txt" 2>&1 || true
config_existed=0
if [ -f /etc/abs-local-models.env ]; then
  sudo cp -a /etc/abs-local-models.env "$backup/abs-local-models.env.before"
  config_existed=1
else
  echo "CONFIG_BACKUP_BLOCKED: /etc/abs-local-models.env does not exist; production config changes will be blocked"
fi

echo "=== SAFE ALIAS AUDIT ==="
# Compare the alias digest against every canonical Ministral entry; the API can
# contain more than one same-name record, so collapsing by name is unsafe.
alias_decision="$(python3 - "$backup/ollama-tags-before.json" <<'PY'
import json,sys
models=json.load(open(sys.argv[1])).get("models",[])
alias_name="llamacpp:316262d960e27504463e6270bd8c1e8665c957ef2cff620ba333af9e1480df63"
aliases=[x for x in models if x.get("name")==alias_name]
canonical_digests={x.get("digest") for x in models if x.get("name")=="ministral-3:3b" and x.get("digest")}
if len(aliases)==1 and aliases[0].get("digest") and aliases[0]["digest"] in canonical_digests:
    print("remove")
else:
    print("keep")
PY
)"
if [ "$alias_decision" = remove ]; then
  alias_tag='llamacpp:316262d960e27504463e6270bd8c1e8665c957ef2cff620ba333af9e1480df63'
  ollama show "$alias_tag" --modelfile > "$backup/ministral-alias.modelfile" 2>&1 || true
  if ollama rm "$alias_tag"; then
    echo "CLEANUP_PASS: removed exact-digest Ministral alias only; canonical tag retained"
  else
    echo "CLEANUP_FAIL: exact-digest alias removal failed; no other tag touched"
  fi
else
  echo "CLEANUP_SKIPPED: alias not proven to match any canonical Ministral digest"
fi

echo "=== CONDITIONAL PHI INSTALL ==="
free_bytes="$(df -B1 --output=avail / | tail -n 1 | tr -d ' ')"
available_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)"
if [ "$free_bytes" -ge 4500000000 ] && [ "$available_kb" -ge 3500000 ]; then
  if ollama list | awk 'NR>1 {print $1}' | grep -Fxq 'phi4-mini:3.8b'; then
    echo "PHI_ALREADY_INSTALLED"
  elif timeout 900 ollama pull phi4-mini:3.8b; then
    echo "PHI_PULL_PASS"
  else
    echo "PHI_PULL_FAIL: retained all existing models; no forced cleanup"
  fi
else
  echo "PHI_PULL_SKIPPED: disk must have >=4.5 GB free and MemAvailable >=3.5 GB"
fi

echo "=== SEQUENTIAL DIRECT SMOKE TESTS ==="
# Test one model at a time with 2048 context, short output and keep_alive=0.
# Thresholds include a small OS/ABS margin; a skipped model is not counted as PASS.
test_model() {
  model="$1"; marker="$2"; min_mb="$3"; timeout_s="$4"
  echo "--- MODEL $model ---"
  if ! ollama list | awk 'NR>1 {print $1}' | grep -Fxq "$model"; then
    echo "RESULT SKIP_NOT_INSTALLED model=$model"
    return
  fi
  available_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)"
  if [ "$available_kb" -lt "$((min_mb * 1024))" ]; then
    echo "RESULT SKIP_MEMORY model=$model available_mb=$((available_kb / 1024)) required_mb=$min_mb"
    return
  fi
  before="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)"
  payload="$(python3 - "$model" "$marker" <<'PY'
import json,sys
print(json.dumps({"model":sys.argv[1],"prompt":"Reply with exactly "+sys.argv[2]+" and nothing else.","stream":False,"think":False,"keep_alive":0,"options":{"num_ctx":2048,"num_predict":40,"temperature":0}}))
PY
)"
  response="$(curl -sS --max-time "$timeout_s" http://127.0.0.1:11434/api/generate -H 'Content-Type: application/json' -d "$payload" 2>&1)"
  rc=$?
  after="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)"
  if [ "$rc" -eq 0 ] && printf '%s' "$response" | python3 -c 'import json,sys; d=json.load(sys.stdin); expected=sys.argv[1].upper(); actual=(d.get("response") or "").strip().upper(); assert expected in actual, {"expected":expected,"actual":actual}; print("response="+actual[:160])' "$marker"; then
    echo "RESULT PASS model=$model before_mb=$((before / 1024)) after_mb=$((after / 1024))"
  else
    echo "RESULT FAIL model=$model curl_rc=$rc before_mb=$((before / 1024)) after_mb=$((after / 1024)) response=$(printf '%s' "$response" | head -c 800)"
  fi
  curl -fsS --max-time 5 http://127.0.0.1:11434/api/ps || true
  echo
}
test_model 'qwen3.5:0.8b' 'ABS_QWEN08_OK' 1200 90
test_model 'qwen3.5:2b' 'ABS_QWEN2B_OK' 2600 150
test_model 'qwen3.5:4b' 'ABS_QWEN4B_OK' 3400 300
test_model 'ministral-3:3b' 'ABS_MINISTRAL3B_OK' 3000 300
test_model 'hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S' 'ABS_GEMMA_E2B_Q3_OK' 3200 300
test_model 'phi4-mini:3.8b' 'ABS_PHI4MINI_OK' 3200 300

echo "=== DIRECT TEST SUMMARY ==="
grep '^RESULT ' "$log" || true
pass_count="$(grep '^RESULT PASS ' "$log" | sed -E 's/.*model=([^ ]+).*/\1/' | sort -u | wc -l | tr -d ' ')"
echo "DIRECT_PASS_COUNT=$pass_count/6"

# Integration is applied only if every selected model passed the direct smoke.
if [ "$pass_count" -eq 6 ] && [ "$config_existed" -eq 1 ]; then
  echo "=== BACKUP AND APPLY SIX-MODEL CONFIG ==="
  [ -f /etc/abs-local-models.env ] && sudo cp -a /etc/abs-local-models.env "$backup/abs-local-models.env.pre-change"
  sudo tee /etc/abs-local-models.env >/dev/null <<'ENV'
ABS_LOCAL_AI_MODELS=qwen3.5-0.8b|http://127.0.0.1:11434|qwen3.5:0.8b,qwen3.5-2b|http://127.0.0.1:11434|qwen3.5:2b,qwen3.5-4b|http://127.0.0.1:11434|qwen3.5:4b,ministral-3b|http://127.0.0.1:11434|ministral-3:3b,gemma4-e2b-q3|http://127.0.0.1:11434|hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S,phi4-mini-3.8b|http://127.0.0.1:11434|phi4-mini:3.8b
ABS_LOCAL_AI_URL=http://127.0.0.1:11434
ABS_LOCAL_AI_MODEL=qwen3.5:0.8b
ABS_LOCAL_AI_MAX_TOKENS=64
ABS_LOCAL_AI_TEMPERATURE=0
ABS_LOCAL_AI_THINK=false
ENV
  sudo systemctl restart abs.service
  sleep 3
  integration_ok=0
  integration_total=0
  test_abs_model() {
    cap="$1"; marker="$2"; integration_total=$((integration_total+1))
    json="$(curl -sS --max-time 300 -X POST http://127.0.0.1:8787/chat -H 'Content-Type: application/json' -d "$(python3 - "$cap" "$marker" <<'PY'
import json,sys
print(json.dumps({"message":"Reply with exactly "+sys.argv[2]+" and nothing else.","approved":True,"context":{"capability_id":"local-ai:"+sys.argv[1],"max_tokens":24,"temperature":0,"think":False,"keep_alive":0,"timeout":280}}))
PY
)" 2>&1)"
    if printf '%s' "$json" | python3 -c 'import json,sys; d=json.load(sys.stdin); cap=sys.argv[1]; marker=sys.argv[2].upper(); p=d.get("provenance") or []; p=p if isinstance(p,list) else [p]; assert d.get("work_state")=="completed", d; assert marker in str(d.get("response","")).upper(), d; assert any(isinstance(x,dict) and x.get("capability_id")=="local-ai:"+cap for x in p), p; print("ABS_INTEGRATION_PASS "+cap)' "$cap" "$marker"; then
      integration_ok=$((integration_ok+1))
    else
      echo "ABS_INTEGRATION_FAIL capability=$cap detail=$(printf '%s' "$json" | head -c 1000)"
    fi
    curl -fsS --max-time 5 http://127.0.0.1:11434/api/ps || true
    echo
  }
  test_abs_model 'qwen3.5-0.8b' 'ABS_QWEN08_OK'
  test_abs_model 'qwen3.5-2b' 'ABS_QWEN2B_OK'
  test_abs_model 'qwen3.5-4b' 'ABS_QWEN4B_OK'
  test_abs_model 'ministral-3b' 'ABS_MINISTRAL3B_OK'
  test_abs_model 'gemma4-e2b-q3' 'ABS_GEMMA_E2B_Q3_OK'
  test_abs_model 'phi4-mini-3.8b' 'ABS_PHI4MINI_OK'
  echo "ABS_INTEGRATION_COUNT=$integration_ok/$integration_total"
  if [ "$integration_ok" -ne 6 ]; then
    echo "ROLLBACK: restore previous local model config"
    if [ -f "$backup/abs-local-models.env.pre-change" ]; then
      sudo cp -a "$backup/abs-local-models.env.pre-change" /etc/abs-local-models.env
      sudo systemctl restart abs.service
      sleep 3
      echo "ROLLBACK_CONFIG_RESTORED"
    fi
  else
    echo "=== SAFE REDUNDANT VARIANT CLEANUP ==="
    cleanup_before_bytes="$(df -B1 --output=avail / | tail -n 1 | tr -d ' ')"
    for tag in \
      'gemma4:e2b' \
      'gemma4:e4b' \
      'gemma4-e4b-iq2m-ctx1k:latest' \
      'hf.co/bartowski/google_gemma-4-E4B-it-GGUF:IQ2_M' \
      'hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q3_K_S'
    do
      referenced="$(python3 - "$tag" /etc/abs-local-models.env <<'PY'
import sys
tag, path = sys.argv[1:]
try:
    text = open(path, encoding="utf-8").read()
except OSError:
    print("unknown")
    raise SystemExit
models = []
for line in text.splitlines():
    if line.startswith("ABS_LOCAL_AI_MODELS="):
        for spec in line.split("=", 1)[1].split(","):
            parts = spec.split("|")
            if len(parts) == 3:
                models.append(parts[2])
print("yes" if tag in models else "no")
PY
)"
      if [ "$referenced" != "no" ]; then
        echo "CLEANUP_KEEP tag=$tag reason=config_reference_or_unknown"
      elif ollama list | awk 'NR>1 {print $1}' | grep -Fxq "$tag"; then
        slug="$(printf '%s' "$tag" | tr '/:' '__')"
        if ollama show "$tag" --modelfile > "$backup/removed-$slug.modelfile" 2>&1; then
          if ollama rm "$tag"; then
            echo "CLEANUP_REMOVED tag=$tag modelfile_backup=$backup/removed-$slug.modelfile"
          else
            echo "CLEANUP_FAIL tag=$tag reason=ollama_rm_failed"
          fi
        else
          echo "CLEANUP_KEEP tag=$tag reason=manifest_backup_failed"
        fi
      else
        echo "CLEANUP_SKIP tag=$tag reason=exact_tag_absent"
      fi
    done
    cleanup_after_bytes="$(df -B1 --output=avail / | tail -n 1 | tr -d ' ')"
    echo "CLEANUP_PHYSICAL_BYTES_DELTA=$((cleanup_after_bytes - cleanup_before_bytes))"
  fi
else
  if [ "$pass_count" -ne 6 ]; then
    echo "INTEGRATION_NOT_APPLIED: direct model passes=$pass_count/6; production model configuration preserved"
  else
    echo "INTEGRATION_NOT_APPLIED: no verified backup of /etc/abs-local-models.env; production config preserved"
  fi
fi

echo "=== FINAL STATE ==="
curl -fsS --max-time 10 http://127.0.0.1:8787/health || true
curl -fsS --max-time 10 http://127.0.0.1:8787/v3/status || true
free -h
df -h /
curl -fsS --max-time 5 http://127.0.0.1:11434/api/ps || true
echo "BACKUP_DIR=$backup"
echo "ABS_LOCAL_AI_FULL_OPERATION_END"
