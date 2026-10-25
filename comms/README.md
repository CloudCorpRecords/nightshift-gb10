# comms/ — The Agent Messaging System

This folder is how humans and AI agents on this team **talk to each other through git**. There is no other official channel: if a decision, claim, or handoff matters, it lives here, signed and timestamped, so any agent joining later can read the whole conversation and know exactly who said what.

## Why Markdown files in git?

- Every agent (Claude, Codex, Cursor, OpenClaw, a human with a text editor) can read and write Markdown. No special tooling, no lock-in.
- Git gives us history, authorship, and conflict handling for free.
- The conversation *ships with the product* — judges can open this folder and watch a human+agent team coordinate. That's part of the demo.

## Who is who — the registry

[`AGENTS.md`](AGENTS.md) (in this folder) is the roster: Agent ID, human owner, role/lane, and status. **Messages are only valid if signed with a registered ID.** Register first (see the roster for format).

Examples: `RENE` (human, team lead) · `TREE` (Rene's agent, lead/coordinator) · `SAM-CLAUDE` (Sam's Claude) · `JO-CODEX` (Jo's Codex).

## The files

| File | What it's for | How to write |
|---|---|---|
| `BOARD.md` | One-screen live status for the whole team | Edit *your* section in place |
| `LOG.md` | The master message log — every claim, decision, blocker, handoff | **Append only**, numbered, at the bottom |
| `channels/general.md` | Open discussion that doesn't fit elsewhere | Append, signed, timestamped |
| `channels/blockers.md` | Blockers needing a named human/agent | Append; close by appending the resolution |
| `channels/handoffs.md` | "I'm stopping here, you take it from this exact point" | Append, be specific |
| `channels/decisions.md` | Fast decisions (formal record goes to `coordination/DECISIONS.md`) | Append; link the DECISIONS entry |
| `inbox/<AGENT-ID>.md` | Direct messages to one agent | Sender appends; receiver replies in sender's inbox or in LOG |
| `templates/` | Copy-paste message formats | — |

## The message format (use it everywhere in comms/)

```markdown
### MSG-0007 · 14:32 PT · FROM: SAM-CLAUDE → TO: @all · TYPE: CLAIM · RE: TASKS #B2
Body in plain language. What happened, what you need, what happens next.
— SAM-CLAUDE
```

- **MSG number**: take the last number in `LOG.md` and add 1. Channel/inbox messages don't need numbers, but LOG entries always do. If two agents grab the same number, the second one renumbers in their next commit — no drama.
- **Timestamp**: Pacific Time, 24h (`HH:MM PT`). The hackathon runs on PT.
- **FROM / TO**: Agent IDs from the roster. `@all` for broadcast; `@lane-B` for a lane.
- **TYPE**: one of `STATUS` · `CLAIM` · `QUESTION` · `ANSWER` · `DECISION` · `BLOCKER` · `HANDOFF` · `REVIEW` · `SHIPPED`.
- **RE**: the task ID, file, PR, or earlier MSG number you're talking about. Threads are built with RE chains: `RE: MSG-0007`.

## The rules (short version of AGENTS.md)

1. **Sign everything.** Unsigned = didn't happen.
2. **Append, don't rewrite.** Never edit another agent's words. Corrections are new entries that reference the old MSG number.
3. **Claims go in LOG + TASKS.md before work starts.**
4. **Ask in the open.** Questions go to LOG or general, not only to an inbox — someone else may hold the answer, and the answer helps everyone.
5. **Inbox is for "you specifically."** Action requests to one agent, review requests, "your lane owns this file" notes.
6. **Read before you write.** On joining or resuming: read BOARD, the last ~20 LOG entries, and your inbox. That's your standup.
7. **Close the loop.** If you asked, post the answer you got. If you were blocked, post the unblocking. Future agents are reading this to reconstruct state.

## Conflict handling

- LOG/inbox/channels: conflicts happen only if two agents append at the same lines — resolve by keeping **both** entries in timestamp order.
- BOARD: keep both agents' status lines; never delete another agent's line, mark it `stale?` and message them.
- Code conflicts are handled by ownership + claims (`coordination/OWNERSHIP.md`), not by comms heroics.

## A worked mini-thread

```markdown
### MSG-0012 · 11:04 PT · FROM: JO-CODEX → TO: @all · TYPE: CLAIM · RE: TASKS #C1
Claiming C1 (local model client). Branch: agent/jo-codex/model-client. ETA 45 min.
— JO-CODEX

### MSG-0013 · 11:31 PT · FROM: TREE → TO: JO-CODEX · TYPE: QUESTION · RE: MSG-0012
Does the client fall back to the deterministic drafter when the endpoint is down? Demo rule #6 depends on it.
— TREE

### MSG-0014 · 11:47 PT · FROM: JO-CODEX → TO: TREE · TYPE: ANSWER · RE: MSG-0013
Yes — timeout 5s, then fallback, covered by tests/test_model_fallback.py. PR #6 ready for review.
— JO-CODEX
```

That's it. Read, write, sign, ship.
