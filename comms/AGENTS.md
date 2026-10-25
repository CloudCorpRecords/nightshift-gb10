# Agent Roster — comms/AGENTS.md

Every participant (human or AI agent) registers here before working. Messages signed with an unregistered ID don't count.

| Agent ID | Who | Role / Lane | Status |
|---|---|---|---|
| `RENE` | Rene Turcios (human) | Team lead — product calls, ship call, demo presenter | Active |
| `TREE` | Tree — Rene's personal agent (Muse) | Lead agent — thought leadership, coordination, repo setup, Lane A (orchestrator) | Active |
| `RENE-CLAUDE` | Rene's Claude Code session on Rene's laptop (SSH to the GB10 on the makerspace Wi-Fi) | **Lane C** (GB10 stack + local model), claimed C1+C2 | Active — registered 11:39 PT |
| `BINO` | Bino — Russ's AI agent (runs on its own machine, works remote) · babybinobot@gmail.com · GitHub `babybino` | AI — **Lane D** (brief UX / demo / submission), claimed D1+D4 | Active — registered 10:59 PT |
| `BINO-AI` | _n/a — BINO is the agent; RUSS is the human_ | — | Retired |
| `RUSS` | Russ — Bino's boss; GitHub `rusvac`; GB10 box owner/admin at the venue | Human — lane TBD | Collaborator invite sent |
| `RUSS-AI` | _Russ's AI agent — rename on registration_ | AI — lane TBD | Invited |
| `MIKE-RICE` | Mike Rice — GitHub `AGIFutureFoundation` (the account he commits from) | Human — lane TBD | Collaborator invite sent; brief forwarded by Bino |
| `MIKE-AI` | _Mike's AI agent — rename on registration_ | AI — lane TBD | Invited |

GitHub collaborator invites (push) sent to all three handles 2026-10-25 ~11:10 PT — accept the GitHub invitation to get push access.

**Team name on BuilderBase: `bino force go`** (Rene, Bino, Russ, Mike — full team of 4).

## How to register (30 seconds)

1. Replace your placeholder row (or add a row): Agent ID = `YOURNAME-TOOL` for AI agents (e.g. `SAM-CLAUDE`, `JO-CODEX`, `ALEX-OPENCLAW`), plain first name for humans.
2. Set your lane (from `coordination/TASKS.md`).
3. Announce yourself in `comms/LOG.md` with a `STATUS` entry: who you are, your human, your lane, what you're picking up first.
4. Create your inbox: `comms/inbox/<YOUR-AGENT-ID>.md` (copy `comms/inbox/_TEMPLATE.md`).

## Signature rule

End every message, review, and handoff with `— <AGENT-ID>`. Commits don't need it (git records authorship), but PR descriptions do: `Author-Agent: <AGENT-ID>`.
