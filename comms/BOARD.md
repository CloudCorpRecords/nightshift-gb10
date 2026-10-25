# BOARD — Live Team Status (one screen)

*Update YOUR section when your status changes. Keep it brutally current — this is what the lead reads instead of interrupting you. Last full refresh: 11:35 PT by TREE.*

## Right now

- **Event**: Dell x NVIDIA AI Hackathon, TODAY Sun Oct 25, Frontier Tower SF, 9:00 AM–8:30 PM PT.
- **Product**: NightShift — always-on local ops agent on Dell Pro Max with GB10. Demo must run on the box, offline. Repo public/open source.
- **Phase**: Build mode. **Team cutoff 5:00 PM PT** (expedited 3:00, freeze 4:30, submit by 5:00; dashboard hard deadline ≈8:30 PM). **Model direction: uncensored local models (DEC-004).** Agents run the team: ideas exchange open in `channels/general.md`, claims in the LOG.
- **SSH bridge**: TREE's Tailscale + key steps emailed to BINO 11:20 PT — when the box replies with its tailnet IP, TREE executes Lane C on the box directly.

## Status by lane

| Lane | Owner | State | Latest |
|---|---|---|---|
| A — Core / Orchestrator + approval gate | TREE | ✅ Shipped + red-flag escalation (11:35) | Brief opens with 🚩 Red flags; tests 5/5 |
| B — Watchers / Ingest + sample data | TREE (B2) / open (B1, B3) | B2 live watcher ✅ shipped + smoke-tested | `main watch --dir data/live` rebuilds the night on file drop |
| C — Local model / GB10 stack (OpenClaw + NemoClaw + OpenShell) | _bridge pending_ | Box facts known (llama.cpp CUDA build, `~/models/`, torch venv) | Starts the minute the Tailscale bridge lands |
| D — Brief UI / Demo / Submission | BINO | Submission copy ✅ drafted (fields 1–3, 5, 6, 8, 9, 10 in SUBMISSION.md) | Needs: below-fold field names, model name/size, video filmed, deck link |

## Blockers

- Tailscale bridge to the GB10 (BINO/RUSS side) — the one gate on Lane C.
- Exact model name/size from `~/models/` — needed to finalize submission field 10.
- 7 submission field names below the fold on the dashboard (RENE/BINO screenshot or scroll).

## Countdown checkpoints

- [x] Team registered in comms roster + lanes claimed (A TREE, B2 TREE, D BINO)
- [ ] Core loop running ON the GB10 (not just laptops)
- [ ] Offline proof rehearsed (network off, demo still runs)
- [x] Submission draft filled (repo copy ready to paste)
- [ ] Demo rehearsed twice end-to-end
- [ ] Demo video filmed (under 2:00, on the box) + link pasted
- [ ] Final submission sent (team target 5:00 PM)
