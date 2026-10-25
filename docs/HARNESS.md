# HARNESS — running NightShift smoothly on the box's agent stack

*Why this doc exists (RENE, 12:38 PT): the demo has to run on one of the
hackathon harnesses, and the agent+model layer must not be the thing that
dies on stage. This is the smoothness plan: harness wiring, a readiness
gate, a watchdog, and the fallback ladder — in that order.*

## 1. The harness: OpenClaw runs the agents, the model stays local

NightShift's five agents run under **OpenClaw** (the hackathon runtime) on
the GB10, with **NemoClaw** as the agent framework layer and **OpenShell**
as the sandbox. The wiring that matters:

- OpenClaw's model provider points at the box's own vLLM —
  base URL `http://localhost:8000/v1`, model id `qwen36`
  (Qwen3.6-35B-A3B-heretic NVFP4). No cloud endpoint is configured,
  anywhere, on purpose.
- The API key is read from the box-local file (`~/Downloads/vllm-api-key.txt`)
  into the environment at launch — never written into the repo or any
  config file that gets committed.
- NightShift's deterministic core runs *under* the harness as the
  guaranteed path: if the model layer is down, the harness still produces
  the brief from templates (see §4).

## 2. OpenShell policy (the gate, stated as rules)

- Egress: deny all, except `localhost:8000` (the model) — the agents
  physically cannot phone home.
- Filesystem: read the night's drop folders + local runbooks; write only
  `outputs/` (brief, queue, receipts).
- Actions: drafting is free; **sending does not exist** — there is no
  send tool in the sandbox for an agent to call. The human approval CLI
  runs outside the agent sandbox, by design.

## 3. Readiness gate — never start a demo on a hope

`scripts/ready-check.sh` (run on the box): verifies the endpoint answers,
`qwen36` is the served model, and a real 1-token completion succeeds
**with** the API key — the exact check that catches the keyed-endpoint
401 trap (an unkeyed client gets 401s and the Drafter silently falls
back to templates: the demo "works" but the model never speaks).
GO / NO-GO, one screen, ~10 seconds once warm.

## 4. Watchdog + fallback ladder

`scripts/model-keepalive.sh` in a tmux session polls the endpoint every
20s, keeps a one-line status at `~/nightshift-ops/status.txt`, and — only
if `SERVE_CMD` is set to the box's serve command — restarts the server
after 3 consecutive failures. It never invents a restart command;
Russ's auto-serve owns starting vLLM.

The ladder, top to bottom — the demo survives every rung:
1. vLLM + qwen36 live (full model drafts).
2. Endpoint hiccup → watchdog restarts; brief still renders.
3. Model down hard → deterministic template drafts (the product's
   designed fallback; the brief says so honestly via `last_error`).
4. Box down entirely → the brief + receipts from the last good run,
   printed backup (Lane D keeps it within arm's reach).

## 5. Env the live run uses (on the box)

```
NIGHTSHIFT_MODEL_URL=http://localhost:8000/v1
NIGHTSHIFT_MODEL_KEY=<read from ~/Downloads/vllm-api-key.txt at launch>
```
(`model.py` sends `Authorization: Bearer $NIGHTSHIFT_MODEL_KEY` when set —
Bino's catch, fixed in the model client.)
