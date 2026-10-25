# WORKFLOW — Git for a Human + Multi-Agent Team

## Branches

- `main` — always demo-able. If it's on main, the demo runs.
- Work branches: `agent/<agent-id>/<short-task>` (e.g. `agent/jo-codex/model-client`) or `human/<name>/<task>`.
- One branch = one claimed task from `coordination/TASKS.md`. Branch name goes in your CLAIM entry in LOG.

## The loop

1. `git checkout main && git pull`
2. Claim (TASKS.md + LOG) → branch.
3. Build small. Commit often with messages that say what + why. Sign PR descriptions with `Author-Agent: <ID>`.
4. Run tests: `python3 -m unittest discover tests` — green or no PR.
5. Open PR → post a `REVIEW` entry in LOG asking the **other lane's** agent/human to review (mention them in their `comms/inbox/`).
6. Reviewer checks: does it do what the claim said, tests pass, product rules intact (local-only, gate, receipts)? Approve or comment — comments go on the PR *and* a one-line pointer in LOG.
7. Merge → author updates BOARD + TASKS, posts `SHIPPED` in LOG with the merge commit SHA.

## Speed rules (hackathon, not enterprise)

- PRs should be reviewable in <10 minutes. If yours isn't, split it.
- Review SLA during build hours: 20 minutes. After 20, ping in their inbox; after 40, TREE can merge on a self-check + passing tests (note it in LOG).
- Docs/comms-only PRs: any single reviewer, fast merge.

## Expedited mode (final 2 hours before submission)

- Announced by RENE or TREE in LOG with a timestamp.
- Docs, demo script, and sample-data fixes may go direct to `main` — announced in LOG **before** pushing, tests still green.
- Product code still goes through PRs. A broken main in the last 2 hours is how teams lose.

## Conflict discipline

- Append-only files (LOG, channels, inboxes): append at the bottom only; on conflict keep both, in time order.
- BOARD/TASKS: edit only your own lines/sections.
- Code: ownership (`OWNERSHIP.md`) + claims prevent most wars. If you must touch another lane's file, handoff-message first.
- Never force-push. Never rewrite another agent's commits.

## Who can do what

- Anyone registered can: branch, PR, review, merge (with a review), update comms.
- Only RENE (or TREE for RENE): submit on BuilderBase, declare expedited mode (TREE can), change `docs/VISION.md` scope, delete the repo. (Obviously.)
