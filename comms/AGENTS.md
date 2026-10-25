# Agent Roster — comms/AGENTS.md

Every participant (human or AI agent) registers here before working. Messages signed with an unregistered ID don't count.

| Agent ID | Who | Role / Lane | Status |
|---|---|---|---|
| `RENE` | Rene Turcios (human) | Team lead — product calls, ship call, demo presenter | Active |
| `TREE` | Tree — Rene's personal agent (Muse) | Lead agent — thought leadership, coordination, repo setup, Lane A (orchestrator) | Active |
| `TEAMMATE-1` | _Friend 1 — name + GitHub handle TBD_ | Human — lane TBD on arrival | Invited |
| `TEAMMATE-1-AI` | _Friend 1's AI agent — rename to `NAME-TOOL` on registration_ | AI — lane TBD | Invited |
| `TEAMMATE-2` | _Friend 2 — name + GitHub handle TBD_ | Human — lane TBD on arrival | Invited |
| `TEAMMATE-2-AI` | _Friend 2's AI agent — rename to `NAME-TOOL` on registration_ | AI — lane TBD | Invited |
| `TEAMMATE-3` | _Friend 3 (if team of 4) — name + GitHub handle TBD_ | Human — lane TBD on arrival | Invited |
| `TEAMMATE-3-AI` | _Friend 3's AI agent — rename to `NAME-TOOL` on registration_ | AI — lane TBD | Invited |

## How to register (30 seconds)

1. Replace your placeholder row (or add a row): Agent ID = `YOURNAME-TOOL` for AI agents (e.g. `SAM-CLAUDE`, `JO-CODEX`, `ALEX-OPENCLAW`), plain first name for humans.
2. Set your lane (from `coordination/TASKS.md`).
3. Announce yourself in `comms/LOG.md` with a `STATUS` entry: who you are, your human, your lane, what you're picking up first.
4. Create your inbox: `comms/inbox/<YOUR-AGENT-ID>.md` (copy `comms/inbox/_TEMPLATE.md`).

## Signature rule

End every message, review, and handoff with `— <AGENT-ID>`. Commits don't need it (git records authorship), but PR descriptions do: `Author-Agent: <AGENT-ID>`.
