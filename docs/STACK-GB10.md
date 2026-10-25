# Stack — Running NightShift on the Dell Pro Max with GB10

*Owner: Lane C. Keep this file truthful: record what actually ran, with versions and exact commands, as you go. Judges and teammates will follow this file.*

## Target stack (from the event brief)

| Layer | Choice | Status |
|---|---|---|
| Hardware | Dell Pro Max with GB10 (venue unit for the day) | ☐ claimed at venue |
| Agent runtime | **OpenClaw** — always-on loop, channels, scheduling | ☐ |
| Agent framework | **NVIDIA NemoClaw** — agent team implementation | ☐ |
| Sandbox / guardrails | **OpenShell** — policy-bound execution, egress deny | ☐ |
| Model | Local open-weight (Nemotron-family first choice) via local OpenAI-compatible server | ☐ |
| Product core | This repo, Python 3 stdlib skeleton | ✅ runs |

## Bring-up order (do it in this order — each step de-risks the next)

1. **Core first (15 min):** clone repo on the GB10, `python3 -m src.nightshift.main run --simulate`, confirm `outputs/morning-brief.md` renders. *Now the demo exists on the box, whatever happens next.*
2. **Model second:** start the local model server (venue-preferred path first), note the endpoint, `export NIGHTSHIFT_MODEL_URL=http://localhost:<port>/v1`, re-run, confirm drafts change + `python3 -m unittest discover tests` still green (includes the fallback test — kill the server, re-run, core must still work).
3. **OpenShell:** wrap the run command in the sandbox with egress denied; run the demo with venue Wi-Fi **off**. Record the policy file under `config/openshell/`.
4. **OpenClaw + NemoClaw:** wire the night loop as an OpenClaw-scheduled job / NemoClaw agents calling the same `src/nightshift` entry points. If this layer fights back, timebox to 90 minutes — the core demo + OpenShell offline proof already satisfies "runs locally on the box"; document what was wired and what wasn't, honestly, in this file.
5. **Bring a model on a drive:** venue Wi-Fi won't survive 40 teams downloading weights. Anything we might load goes on a USB/external drive *before* relying on it (per event guidance).

## Offline proof protocol (the demo's money moment)

1. Show `NIGHTSHIFT_MODEL_URL` pointing at `localhost`.
2. Disable Wi-Fi / pull the cable, on camera, before the run.
3. Run the full simulated night → brief → approval → receipts.
4. Re-enable network only after the pitch segment ends.

## Fallback ladder (if a layer breaks on stage)

- Model server down → deterministic drafter (automatic).
- GB10 unit trouble → same demo on a team laptop, and we say so honestly; keep fighting for the box in parallel (Lane C).
- OpenClaw/NemoClaw wiring incomplete → core loop runs standalone; stack slide describes core as "agent team with OpenClaw/NemoClaw integration in progress" — never claim what isn't running.

## Record your run here

```
Date/time: ____  Machine hostname: ____
Python: ____  Model: ____  Endpoint: ____
OpenClaw ver: ____  NemoClaw ver: ____  OpenShell policy: config/openshell/____
Commands that worked (paste exactly):
...
```
