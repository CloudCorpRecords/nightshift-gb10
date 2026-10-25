# OWNERSHIP — Who Writes Where

Ownership = "ask this lane before changing it" (in their inbox + a LOG note). It prevents parallel edits and merge wars. Within your own lane, move fast.

| Path | Lane | Owner |
|---|---|---|
| `src/nightshift/orchestrator.py`, `main.py`, approval/receipts | A | TREE |
| `src/nightshift/model.py` | C (client contract by A) | Lane C owner |
| `src/nightshift/watchers.py`, `data/` | B | Lane B owner |
| `src/nightshift/triage.py` | B (with A review) | Lane B owner |
| `src/nightshift/research.py` | C | Lane C owner |
| `src/nightshift/draft.py`, `brief.py` | D (drafting prompts with C) | BINO |
| `outputs/` | — generated, never hand-edit | — |
| `docs/STACK-GB10.md`, `config/` | C | Lane C owner |
| `docs/VISION.md`, `README.md` pitch sections | Lead | TREE / RENE |
| `DEMO.md`, `SUBMISSION.md` | D | BINO |
| `comms/BOARD.md` | Everyone edits *own* section | Lead curates |
| `comms/LOG.md`, `channels/`, `inbox/` | Everyone appends | — |
| `coordination/` | Lead | TREE |

Lane C owner: RENE-CLAUDE (since 11:39 PT).

Unclaimed lanes default to TREE until claimed — claim in TASKS.md and this table gets your name.
