# AGENTS.md — Coordination Contract (READ FIRST)

This repo is built by **multiple humans, each with their own AI agent**, working in parallel through git. This file is the contract. If you are an AI agent opening this repo: follow it exactly. If you are a human: this is how you keep the agents from stepping on each other.

## 1. Register before you work

Add yourself to [`comms/AGENTS.md`](comms/AGENTS.md): pick an **Agent ID** (`TREE`, `RENE`, or e.g. `SAM-CLAUDE`, `JO-CODEX` — format: `OWNERNAME-TOOL` for AI agents, plain name for humans). Every message, commit note, and review you leave is signed with that ID. No anonymous work.

## 2. Talk in `comms/` — that is the team's chat

- **`comms/BOARD.md`** — the one-screen status: what is done, in progress, blocked. Update your line whenever your status changes.
- **`comms/LOG.md`** — append-only message log. Every claim, question, decision, blocker, and handoff gets a numbered, signed entry here. **Append at the bottom. Never edit or delete another agent's entry.**
- **`comms/channels/`** — topic threads: `general.md`, `blockers.md`, `handoffs.md`, `decisions.md`.
- **`comms/inbox/<AGENT-ID>.md`** — direct messages to one agent. Write in their inbox; they reply in yours or in LOG.
- Full protocol, message format, and examples: [`comms/README.md`](comms/README.md).

**Rule: if it isn't in comms/, it didn't happen.** Verbal/chat decisions get transcribed into LOG by whoever heard them.

## 3. Claim before you build (non-negotiable)

Before touching code for a task:

1. Check [`coordination/TASKS.md`](coordination/TASKS.md) and [`coordination/OWNERSHIP.md`](coordination/OWNERSHIP.md) — is it claimed? Is the file owned?
2. Add your claim line to TASKS.md and a `CLAIM` entry in `comms/LOG.md`.
3. Only then build. Two agents building the same thing in parallel is the #1 way hackathons die.

## 4. Git workflow (summary — full version in `coordination/WORKFLOW.md`)

- Branch per task: `agent/<agent-id>/<short-task>` (humans: `human/<name>/<task>`).
- **Pull `main` before you start and before you push.** Append-only files (LOG) merge cleanly if everyone appends at the bottom.
- Small PRs, fast reviews: the *other* lane's agent reviews. PR description links the TASKS claim + the LOG message number.
- Green tests or it doesn't merge. `python3 -m unittest discover tests` must pass.
- Final 2 hours before submission: expedited mode (see WORKFLOW.md) — direct-to-main allowed for docs/demo fixes only, announced in LOG first.

## 5. File ownership

`coordination/OWNERSHIP.md` maps each area to a lane. Work outside your lane only via a handoff message in `comms/channels/handoffs.md` + a claim. Ownership prevents merge wars; it is not a wall — ask, and the owner says yes in LOG.

## 6. Product rules (from `docs/VISION.md` — do not violate)

- **Local only.** No cloud API calls in the product path. Ever. (Your own coding tools are your business; the *product* runs offline on the GB10.)
- **The Drafter never sends.** All external actions go through the human approval queue.
- **Every action leaves a receipt** (source + one-line reason + log entry).
- **Demo never dies:** every model call has the deterministic fallback. If it needs the network, it's a bug.

## 7. When you're blocked

Post a `BLOCKER` entry in LOG + `comms/channels/blockers.md` with: what you need, from whom, and what you're doing meanwhile. Then switch to an unblocked task — don't idle, and don't silently work around an owner.

## 8. End of your session

Before you stop: update BOARD, mark your TASKS claims (done / released), and leave a `HANDOFF` entry in LOG saying exactly where you left off and what's next. The next agent — human or AI — starts from your handoff, not from zero.
