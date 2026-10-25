#!/usr/bin/env bash
# One restart-free demo take on the GB10: read-only checks, one sandboxed night, one approval.
# Starts, stops or restarts nothing (box rule 13:40 PT). Record with:
#   script -q --log-timing take.tm --log-out take.out -c 'bash scripts/demo-take.sh'
set -u
export PATH=$HOME/.local/bin:$PATH NO_COLOR=1
SB=nightshift
KEY=$(cat "$HOME/Downloads/vllm-api-key.txt")
clean() { sed -E 's/\x1b\[[0-9;]*[A-Za-z]//g' | grep -vE '^(→ Using sandbox|\(node:|\(Use `node)'; }
in_sb() { openshell sandbox exec -n "$SB" --timeout 200 --no-tty -- sh -c "$1" 2>&1 | clean; }
beat() { printf '\n\033[1;32m## %s\033[0m\n' "$1"; sleep 1.2; }
cmd() { printf '\033[1;36m$ %s\033[0m\n' "$1"; sleep 0.6; }

beat "1/5  This is the box: Dell Pro Max with GB10"
cmd "hostname; nvidia-smi -L"
hostname; nvidia-smi -L
sleep 1.5

beat "2/5  The model runs here: Qwen3.6-35B-A3B (uncensored, NVFP4) on local vLLM"
cmd "curl localhost:8000/v1/models   # keyed, on this box"
curl -s -m 10 -H "Authorization: Bearer $KEY" localhost:8000/v1/models \
  | python3 -c 'import sys,json; d=json.load(sys.stdin)["data"][0]; print("served model:", d["id"], "| context:", d["max_model_len"], "tokens | owner:", d["owned_by"])'
sleep 1.5

beat "3/5  The agents live in an OpenShell sandbox: egress denied, model route only"
cmd "openshell sandbox list"
openshell sandbox list 2>&1 | clean
cmd "openshell sandbox exec -n nightshift -- sh sandbox-probe.sh   # from INSIDE the sandbox"
in_sb 'for u in https://api.github.com https://integrate.api.nvidia.com/v1/models https://pypi.org/simple/ https://example.com; do printf "%-45s " "$u"; curl -s -m 6 -o /dev/null "$u" && echo REACHABLE || echo BLOCKED; done
printf "%-45s " "https://inference.local/v1 (local qwen36)"; curl -s -m 60 https://inference.local/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"qwen36\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with: model ok\"}],\"max_tokens\":10,\"chat_template_kwargs\":{\"enable_thinking\":false}}" | python3 -c "import sys,json; print(\"ANSWERS:\", json.load(sys.stdin)[\"choices\"][0][\"message\"][\"content\"])"'
sleep 1.5

beat "4/5  OpenClaw's agent runs the night shift (inside the sandbox, on the local model)"
in_sb 'rm -f /sandbox/nightshift-gb10/outputs/*' >/dev/null
cmd "openclaw agent --message-file openclaw-night.txt"
in_sb 'openclaw agent --session-id demo-$(date +%s) --message-file /sandbox/openclaw-night.txt --json > /tmp/agent.json 2>/dev/null
python3 - <<"PY"
import json, re
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
print("agent:", find(d, "finalAssistantVisibleText") or "(no reply)")
print("model:", find(d, "winnerModel") or "?")
PY'
sleep 1.5
cmd "head outputs/morning-brief.md"
in_sb 'cd /sandbox/nightshift-gb10 && sed -n "1,30p" outputs/morning-brief.md'
sleep 3
cmd "grep -A2 'Draft · Reply to billing' outputs/morning-brief.md   # polished by qwen36"
in_sb 'cd /sandbox/nightshift-gb10 && grep -A2 "Draft · Reply to billing" outputs/morning-brief.md | tail -1'
sleep 2.5

beat "5/5  Nothing was sent. A human holds the gate."
cmd "python3 -m src.nightshift.main approve --ids Q1 && tail -3 outputs/receipts.log"
in_sb 'cd /sandbox/nightshift-gb10 && python3 -m src.nightshift.main approve --ids Q1 && tail -3 outputs/receipts.log'
sleep 2
printf '\n\033[1;32mNightShift: the night shift, staffed. Privately, on one GB10.\033[0m\n'
sleep 2
