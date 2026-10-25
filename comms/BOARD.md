# BOARD — Live Team Status (one screen)

*Update YOUR section when your status changes. Keep it brutally current — this is what the lead reads instead of interrupting you. Last full refresh: 09:55 PT by TREE.*

## Right now

- **Event**: Dell x NVIDIA AI Hackathon, TODAY Sun Oct 25, Frontier Tower SF, 9:00 AM–8:30 PM PT.
- **Product**: NightShift — always-on local ops agent on Dell Pro Max with GB10. Demo must run on the box, offline.
- **Phase**: Repo + concept + coordination system live. **Next: team registers, lanes get claimed, build starts.**

## Status by lane

| Lane | Owner | State | Latest |
|---|---|---|---|
| A — Core / Orchestrator + approval gate | TREE | Skeleton shipped | `src/nightshift/` runs the simulated night end-to-end |
| B — Watchers / Ingest + sample data | _unclaimed_ | Ready to claim | Sample night data in `data/sample/` |
| C — Local model / RAG / GB10 stack (OpenClaw + NemoClaw + OpenShell) | _unclaimed_ | Ready to claim | Plan + fallbacks in `docs/STACK-GB10.md` |
| D — Brief UI / Demo / Submission | _unclaimed_ | Ready to claim | Script in `DEMO.md`, checklist in `SUBMISSION.md` |

## Blockers

- None yet. (Post in `channels/blockers.md` + LOG the moment one appears.)

## Countdown checkpoints (fill in exact submit time from BuilderBase dashboard!)

- [ ] Team registered in comms roster + lanes claimed
- [ ] Core loop running ON the GB10 (not just laptops)
- [ ] Offline proof rehearsed (network off, demo still runs)
- [ ] Submission draft filled on BuilderBase
- [ ] Demo rehearsed twice end-to-end
- [ ] Final submission sent
