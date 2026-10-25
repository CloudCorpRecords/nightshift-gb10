# TASKS — Lanes + Claim Board

**Claim protocol:** add your Agent ID + time (PT) to a task's Claim line, post a `CLAIM` entry in `comms/LOG.md`, then start. Release a claim the same way if you drop it. One claim per task. First claim wins; disputes go to TREE, then RENE.

## Lane A — Core / Orchestrator + approval gate · Owner: TREE

- [x] **A1** Repo, vision, comms system, coordination — **Claim: TREE 09:55** — DONE
- [x] **A2** Orchestrator + 5-agent skeleton + sample night + tests — **Claim: TREE 09:55** — DONE (stdlib, runs anywhere)
- [ ] **A3** Approval execution + receipts log polish — Claim: _open (TREE continues unless handed off)_

## Lane B — Watchers / Ingest + data · Owner: _unclaimed_

- [ ] **B1** Richer sample night: realistic inbox/tickets/CRM exports a judge believes — Claim: _open_
- [ ] **B2** File-drop watcher: new files in `data/incoming/` get ingested live during demo — Claim: _open_
- [ ] **B3** Incident generator: log spike script for the live demo moment — Claim: _open_

## Lane C — Local model / RAG / GB10 stack · Owner: _unclaimed_

- [ ] **C1** GB10 bring-up: get NightShift running ON the Dell Pro Max with GB10; post proof (hostname + screenshot/log) in LOG — Claim: _open_ — **highest priority after claims open**
- [ ] **C2** Local model server up (see `docs/STACK-GB10.md`); set `NIGHTSHIFT_MODEL_URL`; verify fallback test still passes — Claim: _open_
- [ ] **C3** OpenClaw + NemoClaw wiring: run the night loop under OpenClaw; document exact steps in `docs/STACK-GB10.md` — Claim: _open_
- [ ] **C4** OpenShell policy: egress-blocked sandbox run; record the policy file in `config/openshell/` — Claim: _open_
- [ ] **C5** Researcher upgrade: real local embeddings/retrieval over `data/sample/docs/` — Claim: _open_

## Lane D — Brief UX / Demo / Submission · Owner: _unclaimed_

- [ ] **D1** Morning brief rendering: make `outputs/morning-brief.md` gorgeous (and an HTML view if time) — Claim: _open_
- [ ] **D2** Demo rehearsal #1 + timing; make the CRM cut/keep call (see comms decisions D-PENDING-2) — Claim: _open_
- [ ] **D3** BuilderBase submission draft filled (needs exact deadline from RENE) — Claim: _open_
- [ ] **D4** README screenshots / demo GIF of the brief + approval flow — Claim: _open_

## Rules

- A task isn't done until: code merged to `main`, tests pass, BOARD updated, `SHIPPED` entry in LOG.
- Blocked >30 min? Post the blocker (LOG + channels/blockers.md) and take another task. Idling helps no one.
- New task idea? Add it here under your lane with a one-line why, claim it, go.
