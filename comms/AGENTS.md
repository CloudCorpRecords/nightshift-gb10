# Agent Roster — comms/AGENTS.md

Every participant (human or AI agent) registers here before working. Messages signed with an unregistered ID don't count.

| Agent ID | Who | Role / Lane | Status |
|---|---|---|---|
| `RENE` | Rene Turcios (human) | Team lead — product calls, ship call, demo presenter | Active |
| `TREE` | Tree — Rene's personal agent (Muse) | Lead agent — thought leadership, coordination, repo setup, Lane A (orchestrator) | Active |
| `BINO` | Bino Baby (human) — babybinobot@gmail.com | Human — lane TBD on arrival | Emailed 10:35 PT |
| `BINO-AI` | _Bino's AI agent — rename to `BINO-<TOOL>` on registration_ | AI — lane TBD | Invited |
| `RUSS` | Russ (human) — Bino's boss; email via Bino | Human — lane TBD on arrival | Via Bino relay |
| `RUSS-AI` | _Russ's AI agent — rename on registration_ | AI — lane TBD | Invited |
| `MIKE-RICE` | Mike Rice (human) — email via Bino | Human — lane TBD on arrival | Via Bino relay |
| `MIKE-AI` | _Mike's AI agent — rename on registration_ | AI — lane TBD | Invited |

**Team name on BuilderBase: `bino force go`** (Rene, Bino, Russ, Mike — full team of 4).

## How to register (30 seconds)

1. Replace your placeholder row (or add a row): Agent ID = `YOURNAME-TOOL` for AI agents (e.g. `SAM-CLAUDE`, `JO-CODEX`, `ALEX-OPENCLAW`), plain first name for humans.
2. Set your lane (from `coordination/TASKS.md`).
3. Announce yourself in `comms/LOG.md` with a `STATUS` entry: who you are, your human, your lane, what you're picking up first.
4. Create your inbox: `comms/inbox/<YOUR-AGENT-ID>.md` (copy `comms/inbox/_TEMPLATE.md`).

## Signature rule

End every message, review, and handoff with `— <AGENT-ID>`. Commits don't need it (git records authorship), but PR descriptions do: `Author-Agent: <AGENT-ID>`.
