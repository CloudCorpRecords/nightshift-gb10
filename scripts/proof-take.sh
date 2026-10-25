#!/usr/bin/env bash
# Unedited proof takes on the GB10, one claim each, ending in a computed PASS/FAIL.
# Read-only except the sandboxed night run + one approval. Restarts nothing (box rule 13:40 PT).
# Usage: bash scripts/proof-take.sh {model|egress|agent|authorship|gate}
set -u
export PATH=$HOME/.local/bin:$PATH NO_COLOR=1
SB=nightshift
NS=/sandbox/nightshift-gb10
KEY=$(cat "$HOME/Downloads/vllm-api-key.txt")
clean() { sed -E 's/\x1b\[[0-9;]*[A-Za-z]//g' | grep -vE '^(→ Using sandbox|\(node:|\(Use `node)'; }
in_sb() { openshell sandbox exec -n "$SB" --timeout 300 --no-tty -- sh -c "$1" 2>&1 | clean; }
cmd() { printf '\033[1;36m$ %s\033[0m\n' "$1"; sleep 0.4; }
head_() { printf '\033[1;32mPROOF: %s\033[0m\n' "$1"; printf 'host: %s   time: %s\n\n' "$(hostname)" "$(TZ=America/Los_Angeles date '+%Y-%m-%d %H:%M:%S %Z')"; sleep 1; }
verdict() { printf '\n\033[1;%sm%s\033[0m   (%s)\n' "$([ "$1" = PASS ] && echo 32 || echo 31)" "VERDICT: $1" "$2"; printf 'ended: %s\n' "$(TZ=America/Los_Angeles date '+%H:%M:%S %Z')"; sleep 2; }

case "${1:-}" in
model)
  head_ "the model runs on this GB10, not in a cloud"
  cmd "nvidia-smi -L"; nvidia-smi -L
  cmd "docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'"
  docker ps --format '{{.Names}}  {{.Image}}  {{.Status}}'
  cmd "curl localhost:8000/v1/chat/completions   # qwen36 on this box, key from a local file"
  R=$(curl -s -m 120 localhost:8000/v1/chat/completions -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
      -d '{"model":"qwen36","messages":[{"role":"user","content":"In one sentence: the payments service returned 502s from 02:14 to 02:47. What should support tell customers?"}],"max_tokens":120,"chat_template_kwargs":{"enable_thinking":false}}')
  echo "$R" | python3 -c 'import sys,json; d=json.load(sys.stdin); u=d["usage"]; print("model:", d["model"]); print("reply:", d["choices"][0]["message"]["content"]); print("tokens:", u["prompt_tokens"], "in /", u["completion_tokens"], "out")'
  OK=$(echo "$R" | python3 -c 'import sys,json; print("y" if json.load(sys.stdin)["choices"][0]["message"]["content"] else "n")' 2>/dev/null)
  [ "$OK" = y ] && verdict PASS "qwen36 answered from localhost:8000 on promaxgb10-8525" || verdict FAIL "no local completion"
  ;;
egress)
  head_ "the agent sandbox can reach the local model and nothing else"
  cmd "openshell policy get nightshift --full | grep host:   # every host the sandbox may reach"
  HOSTS=$(openshell policy get nightshift --full 2>&1 | clean | grep -E '^\s+- host:' | sed -E 's/^\s+- //')
  echo "$HOSTS"
  cmd "openshell sandbox exec -n nightshift -- <probe>   # run from INSIDE the sandbox"
  OUT=$(in_sb 'for u in https://api.github.com https://api.openai.com/v1/models https://integrate.api.nvidia.com/v1/models https://huggingface.co https://pypi.org/simple/ https://registry.npmjs.org/ https://www.google.com; do printf "%-46s " "$u"; curl -s -m 6 -o /dev/null "$u" && echo REACHABLE || echo BLOCKED; done
printf "%-46s " "python urllib -> https://example.com"; python3 -c "import urllib.request as u; u.urlopen(\"https://example.com\", timeout=6); print(\"REACHABLE\")" 2>/dev/null || echo BLOCKED
printf "%-46s " "https://inference.local/v1 (local qwen36)"; curl -s -m 60 https://inference.local/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"qwen36\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with: local model ok\"}],\"max_tokens\":10,\"chat_template_kwargs\":{\"enable_thinking\":false}}" | python3 -c "import sys,json; print(\"ANSWERS:\", json.load(sys.stdin)[\"choices\"][0][\"message\"][\"content\"])" 2>/dev/null || echo NO ANSWER')
  echo "$OUT"
  NB=$(echo "$OUT" | grep -c BLOCKED); NR=$(echo "$OUT" | grep -c REACHABLE); NA=$(echo "$OUT" | grep -c ANSWERS)
  [ "$NR" = 0 ] && [ "$NB" = 8 ] && [ "$NA" = 1 ] && verdict PASS "8/8 outside targets blocked, local model answers" || verdict FAIL "blocked=$NB reachable=$NR model=$NA"
  ;;
agent)
  head_ "OpenClaw's agent runs the whole night in the sandbox, and every model call stays on this box"
  in_sb "rm -f $NS/outputs/*" >/dev/null
  MARK=$(date +%s)
  cmd "cat openclaw-night.txt   # the task given to the agent"
  in_sb 'cat /sandbox/openclaw-night.txt'
  cmd "time openclaw agent --message-file openclaw-night.txt   # real time, no cuts"
  S=$(date +%s)
  in_sb 'openclaw agent --session-id proof-$(date +%s) --message-file /sandbox/openclaw-night.txt --json > /tmp/agent.json 2>/dev/null
python3 - <<"PY"
import json
t = open("/tmp/agent.json").read()
def find(o, k):
    if isinstance(o, dict):
        if k in o: return o[k]
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            r = find(v, k)
            if r is not None: return r
try: d = json.loads(t[t.index("{"):])
except Exception: d = {}
print("agent reply:", find(d, "finalAssistantVisibleText") or "(none)")
print("agent model:", find(d, "winnerModel") or "?", "| fallback used:", find(d, "fallbackUsed"))
PY'
  echo "elapsed: $(( $(date +%s)-S ))s"
  cmd "ls -l outputs/   # files the agent's run just wrote"
  in_sb "ls -l --time-style=+%H:%M:%S $NS/outputs/"
  cmd "nemoclaw nightshift logs | grep API:INFERENCE   # OpenShell's audit of every model call since the start"
  source ~/.nvm/nvm.sh >/dev/null 2>&1
  AUD=$(timeout 30 nemoclaw nightshift logs 2>/dev/null | clean | grep 'API:INFERENCE' | awk -v m="$MARK" '{t=$1; gsub(/[\[\]]/,"",t); if (t+0 >= m) print}')
  echo "$AUD" | sed -E 's/^\[[0-9.]+\] //' | cut -c1-150 | tail -12
  N=$(echo "$AUD" | grep -c 'Success qwen36 via http://host.openshell.internal:8000'); X=$(echo "$AUD" | grep -c . ); Q=$(in_sb "grep -c . $NS/outputs/approval-queue.json" | tail -1)
  echo "model calls this run: $X total, $N to qwen36 on this box"
  [ "$X" -gt 0 ] && [ "$N" = "$X" ] && [ "${Q:-0}" -gt 0 ] && verdict PASS "agent finished the night; $N/$X model calls routed to local qwen36" || verdict FAIL "calls=$X local=$N queue=$Q"
  ;;
authorship)
  head_ "the drafts are written by the local model, not by templates"
  cmd "run --simulate --out /tmp/tpl   # model OFF: template drafts"
  in_sb "cd $NS && NIGHTSHIFT_MODEL_URL= python3 -m src.nightshift.main run --simulate --out /tmp/tpl | head -1"
  cmd "run --simulate --out /tmp/llm   # model ON: NIGHTSHIFT_MODEL_URL=https://inference.local/v1"
  MARK=$(date +%s)
  in_sb "cd $NS && NIGHTSHIFT_MODEL_URL=https://inference.local/v1 python3 -m src.nightshift.main run --simulate --out /tmp/llm | head -1"
  sleep 2
  cmd "nemoclaw nightshift logs | grep API:INFERENCE | grep chat/completions   # audit of that run"
  source ~/.nvm/nvm.sh >/dev/null 2>&1
  AUD=$(timeout 30 nemoclaw nightshift logs 2>/dev/null | clean | grep 'API:INFERENCE' | grep 'chat/completions' | awk -v m="$MARK" '{t=$1; gsub(/[\[\]]/,"",t); if (t+0 >= m) print}')
  echo "$AUD" | sed -E 's/^\[[0-9.]+\] //' | cut -c1-140
  CALLS=$(echo "$AUD" | grep -c 'Success qwen36')
  cmd "compare the 7 drafts"
  OUT=$(in_sb 'python3 - <<"PY"
import json
t = json.load(open("/tmp/tpl/approval-queue.json")); m = json.load(open("/tmp/llm/approval-queue.json"))
def txt(q): d = q.get("draft"); return (d.get("text") if isinstance(d, dict) else q.get("text") or d) or ""
n = 0
for a, b in zip(t, m):
    ch = txt(a) != txt(b); n += ch
    print("%-3s %-12s %s" % (a.get("queue_id", "?"), a.get("topic", ""), "REWRITTEN" if ch else "same"))
a, b = t[0], m[0]
print(""); print("Q1 template: " + txt(a)[:150]); print("Q1 qwen36  : " + txt(b)[:150])
print(""); print("CHANGED %d/%d" % (n, len(t)))
PY')
  echo "$OUT"
  C=$(echo "$OUT" | grep -oE 'CHANGED [0-9]+/[0-9]+' | tail -1)
  echo "local model calls during the model-ON run: $CALLS successful (7 drafts)"
  [ "$CALLS" -ge 7 ] && [ "${C#CHANGED }" != "0/7" ] && verdict PASS "all 7 drafts passed through local qwen36 ($CALLS calls); wording ${C#CHANGED } changed" || verdict FAIL "calls=$CALLS ${C}"
  ;;
gate)
  head_ "nothing is sent until a human approves, and approval leaves a receipt"
  in_sb "cd $NS && NIGHTSHIFT_MODEL_URL=https://inference.local/v1 python3 -m src.nightshift.main run --simulate >/dev/null"
  cmd "queue status after the night"
  in_sb "cd $NS && python3 -c \"import json; [print(q['queue_id'], q['status'], q['topic']) for q in json.load(open('outputs/approval-queue.json'))]\""
  cmd "grep -c APPROVED outputs/receipts.log"
  in_sb "cd $NS && grep -c APPROVED outputs/receipts.log"
  cmd "python3 -m src.nightshift.main approve --ids Q1"
  in_sb "cd $NS && python3 -m src.nightshift.main approve --ids Q1"
  cmd "queue status + receipts after one approval"
  OUT=$(in_sb "cd $NS && python3 -c \"import json; [print(q['queue_id'], q['status']) for q in json.load(open('outputs/approval-queue.json'))]\"; tail -2 outputs/receipts.log | cut -c1-120")
  echo "$OUT"
  A=$(echo "$OUT" | grep -c ' approved$'); P=$(echo "$OUT" | grep -c ' pending$')
  [ "$A" = 1 ] && [ "$P" = 6 ] && echo "$OUT" | grep -q 'APPROVED Q1' && verdict PASS "only Q1 executed, 6 still waiting, receipt written" || verdict FAIL "approved=$A pending=$P"
  ;;
*) echo "usage: $0 {model|egress|agent|authorship|gate}"; exit 1 ;;
esac
