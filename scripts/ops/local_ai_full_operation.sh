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
# A successful response is not a pass unless Ollama confirms the model unloaded.
# Wait for reclaimable memory after keep_alive=0; never lower safety thresholds to force a test.
wait_for_memory() {
  required_mb="$1"; max_wait_s="$2"
  [ -z "$max_wait_s" ] && max_wait_s=90
  attempts=$((max_wait_s / 5))
  [ "$attempts" -lt 1 ] && attempts=1
  attempt=0
  while [ "$attempt" -lt "$attempts" ]; do
    available_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)"
    if [ "$available_kb" -ge "$((required_mb * 1024))" ]; then
      echo "MEMORY_WAIT_PASS available_mb=$((available_kb / 1024)) required_mb=$required_mb waited_s=$((attempt * 5))"
      return 0
    fi
    sleep 5
    attempt=$((attempt + 1))
  done
  available_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)"
  echo "MEMORY_WAIT_TIMEOUT available_mb=$((available_kb / 1024)) required_mb=$required_mb waited_s=$((attempt * 5))"
  return 1
}

assert_unloaded() {
  active_json="$(curl -fsS --max-time 5 http://127.0.0.1:11434/api/ps 2>&1)" || {
    echo "UNLOAD_FAIL reason=api_ps_unavailable"
    return 1
  }
  if printf '%s' "$active_json" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert not d.get("models"), d; print("UNLOAD_PASS models=[]")'; then
    return 0
  fi
  echo "UNLOAD_FAIL active=$(printf '%s' "$active_json" | head -c 500)"
  return 1
}
test_model() {
  model="$1"; marker="$2"; min_mb="$3"; timeout_s="$4"
  echo "--- MODEL $model ---"
  if ! ollama list | awk 'NR>1 {print $1}' | grep -Fxq "$model"; then
    echo "RESULT SKIP_NOT_INSTALLED model=$model"
    return
  fi
  if ! wait_for_memory "$min_mb" 90; then
    echo "RESULT SKIP_MEMORY model=$model"
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
  if [ "$rc" -eq 0 ] && printf '%s' "$response" | python3 -c 'import json,sys; d=json.load(sys.stdin); expected=sys.argv[1].upper(); actual=(d.get("response") or "").strip().upper(); assert expected in actual, {"expected":expected,"actual":actual}; print("response="+actual[:160])' "$marker" && assert_unloaded; then
    echo "RESULT PASS model=$model before_mb=$((before / 1024)) after_mb=$((after / 1024))"
  else
    echo "RESULT FAIL model=$model curl_rc=$rc before_mb=$((before / 1024)) after_mb=$((after / 1024)) response=$(printf '%s' "$response" | head -c 800)"
  fi
  echo
}
test_model 'qwen3.5:0.8b' 'ABS_QWEN08_OK' 1200 90
test_model 'qwen3.5:2b' 'ABS_QWEN2B_OK' 2600 150
test_model 'qwen3.5:4b' 'ABS_QWEN4B_OK' 3400 300
test_model 'ministral-3:3b' 'ABS_MINISTRAL3B_OK' 3000 300
test_model 'hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S' 'ABS_GEMMA_E2B_Q3_OK' 3200 300
test_model 'phi4-mini:3.8b' 'ABS_PHI4MINI_OK' 3200 300

# Complementary capability tests do not alter the six-model chat pass count.
ministral_tool_pass=0
phi_tool_pass=0
gemma_vision_pass=0
qwen_vision_pass=0
test_tool_call() {
  model="$1"; marker="$2"; min_mb="$3"; timeout_s="$4"
  if ! wait_for_memory "$min_mb" 90; then
    echo "TOOL_RESULT SKIP_MEMORY model=$model"
    return
  fi
  payload="$(python3 - "$model" "$marker" <<'PY'
import json,sys
model,marker=sys.argv[1:]
print(json.dumps({
  "model":model,
  "messages":[{"role":"user","content":"You must call the record_test tool, not answer directly. Pass marker exactly as "+marker+"."}],
  "tools":[{"type":"function","function":{"name":"record_test","description":"Record a local capability validation marker.","parameters":{"type":"object","properties":{"marker":{"type":"string"}},"required":["marker"]}}}],
  "stream":False,"think":False,"keep_alive":0,
  "options":{"num_ctx":2048,"num_predict":96,"temperature":0}
}))
PY
)"
  response="$(curl -sS --max-time "$timeout_s" http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d "$payload" 2>&1)"
  rc=$?
  if [ "$rc" -eq 0 ] && printf '%s' "$response" | python3 -c 'import json,sys
d=json.load(sys.stdin); expected=sys.argv[1]; calls=(d.get("message") or {}).get("tool_calls") or []
for call in calls:
 f=call.get("function") or {}; args=f.get("arguments") or {}
 if isinstance(args,str):
  try: args=json.loads(args)
  except Exception: args={}
 if f.get("name")=="record_test" and args.get("marker")==expected:
  print("tool_call=record_test marker="+expected); raise SystemExit(0)
raise SystemExit("expected tool call not returned")' "$marker" && assert_unloaded; then
    echo "TOOL_RESULT PASS model=$model"
    [ "$model" = "ministral-3:3b" ] && ministral_tool_pass=1
    [ "$model" = "phi4-mini:3.8b" ] && phi_tool_pass=1
  else
    echo "TOOL_RESULT FAIL model=$model curl_rc=$rc detail=$(printf '%s' "$response" | head -c 500)"
  fi
  echo
}
test_gemma_vision() {
  model='hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S'
  if ! wait_for_memory 3000 90; then
    echo "VISION_RESULT SKIP_MEMORY model=$model"
    return
  fi
  image_b64="$(python3 - <<'PY'
import base64,struct,zlib
def chunk(kind,data):
    return struct.pack(">I",len(data))+kind+data+struct.pack(">I",zlib.crc32(kind+data)&0xffffffff)
w=h=16
raw=b"".join(b"\x00"+(b"\xff\x00\x00\xff"*w) for _ in range(h))
png=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b"")
print(base64.b64encode(png).decode())
PY
)"
  payload="$(python3 - "$model" "$image_b64" <<'PY'
import json,sys
model,image=sys.argv[1:]
print(json.dumps({
  "model":model,
  "messages":[{"role":"user","content":"Inspect the attached image. If its dominant color is red, reply exactly ABS_GEMMA_VISION_OK; otherwise reply NO.","images":[image]}],
  "stream":False,"think":False,"keep_alive":0,
  "options":{"num_ctx":2048,"num_predict":32,"temperature":0}
}))
PY
)"
  response="$(curl -sS --max-time 300 http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d "$payload" 2>&1)"
  rc=$?
  if [ "$rc" -eq 0 ] && printf '%s' "$response" | python3 -c 'import json,sys
d=json.load(sys.stdin); s=((d.get("message") or {}).get("content") or "").upper(); assert "ABS_GEMMA_VISION_OK" in s, s; print("vision_response="+s[:120])' && assert_unloaded; then
    gemma_vision_pass=1
    echo "VISION_RESULT PASS model=$model"
  else
    echo "VISION_RESULT FAIL model=$model curl_rc=$rc detail=$(printf '%s' "$response" | head -c 500)"
  fi
  echo
}
test_gemma_vision

test_qwen_vision() {
  model='qwen3.5:4b'
  if ! wait_for_memory 3400 90; then
    echo "VISION_RESULT SKIP_MEMORY model=$model"
    return
  fi
  image_b64="$(python3 - <<'PY'
import base64,struct,zlib
def chunk(kind,data):
    return struct.pack(">I",len(data))+kind+data+struct.pack(">I",zlib.crc32(kind+data)&0xffffffff)
w=h=16
raw=b"".join(b"\x00"+(b"\xff\x00\x00\xff"*w) for _ in range(h))
png=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b"")
print(base64.b64encode(png).decode())
PY
)"
  payload="$(python3 - "$model" "$image_b64" <<'PY'
import json,sys
model,image=sys.argv[1:]
print(json.dumps({
  "model":model,
  "messages":[{"role":"user","content":"Inspect the attached image. If its dominant color is red, reply exactly ABS_QWEN_VISION_OK; otherwise reply NO.","images":[image]}],
  "stream":False,"think":False,"keep_alive":0,
  "options":{"num_ctx":2048,"num_predict":32,"temperature":0}
}))
PY
)"
  response="$(curl -sS --max-time 300 http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d "$payload" 2>&1)"
  rc=$?
  if [ "$rc" -eq 0 ] && printf '%s' "$response" | python3 -c 'import json,sys
d=json.load(sys.stdin); s=((d.get("message") or {}).get("content") or "").upper(); assert "ABS_QWEN_VISION_OK" in s, s; print("vision_response="+s[:120])' && assert_unloaded; then
    qwen_vision_pass=1
    echo "VISION_RESULT PASS model=$model"
  else
    echo "VISION_RESULT FAIL model=$model curl_rc=$rc detail=$(printf '%s' "$response" | head -c 500)"
  fi
  echo
}
test_qwen_vision

# Run tool-call checks after vision so one heavy tool test cannot starve image tests.
test_tool_call 'ministral-3:3b' 'ABS_MINISTRAL_TOOL_OK' 3000 300
test_tool_call 'phi4-mini:3.8b' 'ABS_PHI_TOOL_OK' 2800 300

echo "=== DIRECT TEST SUMMARY ==="
grep '^RESULT ' "$log" || true
pass_count="$(grep '^RESULT PASS ' "$log" | sed -E 's/.*model=([^ ]+).*/\1/' | sort -u | wc -l | tr -d ' ')"
echo "DIRECT_PASS_COUNT=$pass_count/6"

# Integration is applied only if every selected model passed the direct smoke.
if [ "$pass_count" -eq 6 ] && [ "$config_existed" -eq 1 ] && [ "$((ministral_tool_pass + phi_tool_pass))" -ge 1 ] && [ "$((gemma_vision_pass + qwen_vision_pass))" -ge 1 ]; then
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
    case "$cap" in
      qwen3.5-0.8b) required_mb=2600 ;;
      qwen3.5-2b) required_mb=3800 ;;
      qwen3.5-4b|ministral-3b) required_mb=4050 ;;
      gemma4-e2b-q3) required_mb=4000 ;;
      phi4-mini-3.8b) required_mb=3700 ;;
      *) required_mb=3000 ;;
    esac
    if ! wait_for_memory "$required_mb" 90; then
      echo "ABS_INTEGRATION_FAIL capability=$cap reason=memory_not_recovered"
      return
    fi
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
      if [ "$tag" = "gemma4:e2b" ] && [ "$gemma_vision_pass" -ne 1 ] && [ "$qwen_vision_pass" -ne 1 ]; then
        echo "CLEANUP_KEEP tag=$tag reason=selected_Gemma_vision_not_proven"
      elif [ "$referenced" != "no" ]; then
        echo "CLEANUP_KEEP tag=$tag reason=config_reference_or_unknown"
      elif ollama list | awk 'NR>1 {print $1}' | grep -Fxq "$tag"; then
        digest="$(python3 - "$backup/ollama-tags-before.json" "$tag" <<'PY'
import json,sys
data=json.load(open(sys.argv[1])).get("models",[])
matches=[x for x in data if x.get("name")==sys.argv[2]]
if len(matches)==1 and matches[0].get("digest"):
    print(matches[0]["digest"])
else:
    print("ambiguous")
PY
)"
        if [ "$digest" = "ambiguous" ]; then
          echo "CLEANUP_KEEP tag=$tag reason=manifest_digest_ambiguous"
          continue
        fi
        slug="$(printf '%s' "$tag" | tr '/:' '__')"
        if ollama show "$tag" --modelfile > "$backup/removed-$slug.modelfile" 2>&1; then
          if ollama rm "$tag"; then
            echo "CLEANUP_REMOVED tag=$tag digest=$digest modelfile_backup=$backup/removed-$slug.modelfile"
          else
            echo "CLEANUP_FAIL tag=$tag digest=$digest reason=ollama_rm_failed"
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
  elif [ "$config_existed" -ne 1 ]; then
    echo "INTEGRATION_NOT_APPLIED: no verified backup of /etc/abs-local-models.env; production config preserved"
  elif [ "$((ministral_tool_pass + phi_tool_pass))" -lt 1 ]; then
    echo "INTEGRATION_NOT_APPLIED: no selected local model proved tool calling; production config preserved"
  elif [ "$((gemma_vision_pass + qwen_vision_pass))" -lt 1 ]; then
    echo "INTEGRATION_NOT_APPLIED: no selected local model proved image input; production config preserved"
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
