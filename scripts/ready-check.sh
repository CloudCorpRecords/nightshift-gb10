#!/usr/bin/env bash
# NightShift readiness gate — run on the GB10 before any demo or live run.
# Prints GO / NO-GO. Checks: endpoint answers, model id is qwen36, and a
# real 1-token completion succeeds WITH the API key (catches the 401 trap
# Bino flagged: a keyed vLLM makes an unkeyed client silently fall back).
set -u
URL="${NIGHTSHIFT_MODEL_URL:-http://localhost:8000/v1}"
KEY_FILE="${NIGHTSHIFT_MODEL_KEY_FILE:-$HOME/Downloads/vllm-api-key.txt}"
AUTH=()
if [ -f "$KEY_FILE" ]; then
  AUTH=(-H "Authorization: Bearer $(cat "$KEY_FILE")")
fi

echo "== models =="
MODELS=$(curl -s --max-time 10 "${AUTH[@]}" "$URL/models") || { echo "NO-GO: endpoint unreachable"; exit 1; }
echo "$MODELS" | head -c 300; echo
echo "$MODELS" | grep -q "qwen36" || { echo "NO-GO: qwen36 not served"; exit 1; }

echo "== completion probe =="
RESP=$(curl -s --max-time 60 "${AUTH[@]}" "$URL/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen36","messages":[{"role":"user","content":"Reply with one word: ready"}],"max_tokens":8,"temperature":0}')
echo "$RESP" | head -c 300; echo
# Content must be non-empty AFTER stripping <think> blocks — a null or
# think-only reply is not a GO (RENE-CLAUDE's catch, MSG-0020).
echo "$RESP" | python3 -c "
import json, sys, re
d = json.load(sys.stdin)
c = d['choices'][0]['message'].get('content') or ''
c = re.sub(r'<think>.*?</think>', '', c, flags=re.S).strip()
sys.exit(0 if c else 1)
" || { echo "NO-GO: completion empty or failed (auth? warm-up? think-only?) — check vLLM log"; exit 1; }
echo "GO: model endpoint is live, keyed, and answering with real content."
