# ROADMAP — NightShift, the self-sufficient offline ops agent

*Direction set by RENE (13:06 PT, hackathon day): NightShift should run
itself, completely offline, and think more like a person — including
deciding for itself when to wake up. This roadmap is the build plan for
that. Today's shipped core (Phase 0) is the seed; everything after it is
ordered so each phase is provable before the next begins.*

## Principles (non-negotiable, inherited from VISION + today's lessons)

1. **Offline is a test, not a claim.** Every phase ships with an
   air-gap proof: a run that fails loudly if any non-localhost socket
   opens. If it needs the network, it's a bug.
2. **Autonomy is earned, never granted.** Every increase in what
   NightShift may do alone is unlocked by measured approval history,
   and every unlock is reversible in one command.
3. **Receipts for everything.** Any action, decision, wake, or skip
   can be replayed: what it saw, what it thought, what it did, why.
4. **The demo never dies** generalizes to: **the night never dies.**
   Every capability has a degraded mode beneath it, down to the
   deterministic core that needs no model at all.
5. **Local first, local only.** Learning happens on the box, from the
   box's own history. Nothing about a company's night ever leaves it.

---

## Phase 0 — The working night (SHIPPED, 2026-10-25)

Five agents (Watcher, Triager, Researcher, Drafter, Briefer) +
approval-gated orchestrator on one GB10. Live local model (vLLM,
qwen36) writes every draft; deterministic core guarantees the pipeline
without it. Red-flag escalation, live drop-folder mode, morning brief
+ approval queue + receipts. Proven: 23 items → 8 clusters → 7 drafts
in ~8 s on the box, Wi-Fi off.

## Phase 1 — Never dies: self-sufficiency of the body

*Goal: the box can be left alone for a month.*

- **Boot integrity:** verify model weight hashes and config on every
  start; a corrupt or swapped model is detected, never silently served.
- **Supervisor hierarchy:** watchdog watches the model server; a
  supervisor watches the watchdog; systemd/tmux units restart any
  layer with backoff and a cap, and every restart lands in the receipts.
- **Power & crash recovery:** the night is a journal, not a run.
  Power loss mid-night resumes from the journal exactly where it
  stopped — no item processed twice, none lost.
- **Resource budgets:** disk, memory, and log growth quotas with
  self-rotation; the box degrades (smaller context, template mode)
  before it ever fills up and dies.
- **Self-test canary:** every wake begins with a synthetic mini-night
  (3 known items with known answers). If the canary fails, NightShift
  says so in the brief instead of pretending the night went fine.
- **Offline lifeline:** updates (models, runbooks, code) arrive on
  signed USB/local media only, verified before install, with
  one-command rollback to the last known-good stack.

**Acceptance:** pull the power mid-run, pull the network for a week,
corrupt a non-essential file — the brief still arrives, honest about
what degraded.

## Phase 2 — Keeps its own hours: wake intelligence

*Goal: NightShift decides when to sleep, doze, and wake — like a good
night-shift human who knows the house's rhythms.*

- **Sleep states:** *Deep sleep* (nothing but a hardware-timer wake),
  *doze* (watcher only, cheap scans of drop folders / local queues),
  *full wake* (the whole pipeline + model). States are chosen, logged,
  and explained in the brief ("I woke at 03:12 because…").
- **Event-driven wakes:** local signals only — a file lands, an
  on-prem webhook fires, an SLA clock crosses a threshold, the local
  mail spool grows. No polling the internet; the house knocks, it wakes.
- **Learned rhythm:** from its own history, NightShift learns when
  work actually arrives (the 01:00 ticket batch, Monday's pile-up,
  the deploy window that always breaks something) and pre-wakes
  *before* predictable peaks instead of reacting after.
- **Urgency calculus:** a doze-scan scores what it sees; a red-flag
  item (churn, legal, breach, safety) forces a full wake immediately,
  any hour. Routine noise never does.
- **Energy & wear budget:** wakefulness costs GPU heat and fan hours;
  the scheduler spends them where the night's risk is, and says what
  it chose not to watch and why.
- **Human-set guardrails:** quiet hours, a hard "never wake for X"
  list, and a morning summary of every wake decision — the human
  tunes the judgment, the agent makes the calls.

**Acceptance:** a two-week simulated calendar (replayed nights with
planted peaks and one 3 AM red flag): NightShift sleeps through the
noise, pre-wakes for the peaks, and is fully awake within a minute of
the red flag — with a wake journal a human can audit line by line.

## Phase 3 — Thinks in passes: deliberation

*Goal: replace one-shot generation with something closer to how a
careful person works a problem.*

- **Draft → doubt → revise:** every consequential draft gets a second
  pass by a critic instance whose only job is to find what's wrong —
  missing facts, wrong tone, invented details — before the human ever
  sees it. The brief shows the final draft; the receipts keep both.
- **Calibrated uncertainty:** each draft and cluster carries a
  confidence with reasons. Low confidence doesn't guess harder; it
  escalates — the item leads the brief with "I don't know, here's
  what I checked" instead of a confident fabrication.
- **Fact discipline:** every factual sentence in a draft must trace to
  a night item or a runbook line (citation-checked mechanically, the
  way our research threshold already works). Untraceable claims are
  cut or flagged, never smoothed over.
- **Counterfactual check:** before recommending an action, the
  Researcher must answer "what would make this the wrong call?" and
  attach the answer.
- **End-of-night reflection:** after the brief is rendered, a
  reflection pass re-reads the whole night: what did I miss, what's
  still open, what will the morning bring? Its output becomes
  tomorrow's watch-list — the agent hands *itself* a handoff.

**Acceptance:** a seeded "nasty night" suite (contradictory tickets, a
plausible-but-wrong runbook, a customer who is angry *and* mistaken):
no untraceable factual claims survive, the wrong-runbook trap is
caught by the counterfactual pass, and confidence scores track
reality (calibration measured, not vibes).

## Phase 4 — Learns the house: memory that compounds

*Goal: month three's NightShift is visibly better than day one's —
trained by the house, on the house's data, never leaving the box.*

- **Approval-diff learning:** every human edit to a draft is a lesson.
  NightShift diffs what it wrote against what the human sent, distills
  house rules ("we never promise refunds in the first reply; we call
  them 'account credits'"), and applies them — each rule visible,
  editable, deletable by the human.
- **Episodic memory:** every night is remembered and searchable
  locally: "third time this integration broke on a Sunday" is a fact
  the agent can cite, because it kept the receipts.
- **People sense:** per-customer and per-team history shapes triage
  and tone — the VIP who is actually at-risk, the reporter whose
  "urgent" never is — learned from outcomes, always inspectable,
  never a black box score a human can't challenge.
- **Playbook crystallization:** a fix that worked three times becomes
  a candidate playbook; the human approves it once, and it runs as
  procedure thereafter (with the same approval gates on actions).
- **Forgetting:** memory has retention rules — stale contacts decay,
  resolved grudges expire, and the human can order anything forgotten
  and watch it happen in the receipts.

**Acceptance:** replay month one's nights against month three's
NightShift: drafts need measurably fewer human edits, known-repeat
incidents are pre-clustered with their history attached, and every
learned rule in force can be listed and explained on one screen.

## Phase 5 — Earns the keys: graduated autonomy

*Goal: the approval queue shrinks to the decisions that deserve a
human — and only those.*

- **Per-category trust ladder:** categories (e.g., password-reset
  replies, status-page updates, duplicate-ticket closes) climb from
  *draft-only* → *draft + recommended* → *auto-send with instant
  recall window* → *auto-send*, each step unlocked by a measured
  streak of unedited approvals (default: 50) and revoked by a single
  human correction.
- **Blast-radius caps:** even trusted categories carry budgets —
  max sends per night, max recipients, never two auto actions on the
  same thread — so a bad night is a small night.
- **Kill switch & morning veto:** one command freezes all autonomy
  back to draft-only; the brief always lists what was auto-done with
  one-click undo where the platform allows it.
- **Adversarial self-drills:** locally generated attack nights
  (prompt-injection tickets, a fake "CEO" demanding a wire, social
  engineering in a support thread) run against the current build
  monthly. Any drill failure drops the affected category back down
  the ladder automatically.

**Acceptance:** a category only auto-sends after its streak is proven
in the log; the drill suite passes; and a simulated bad-model night
(wrong drafts at scale) is contained by the caps with a complete
receipt trail.

## Phase 6 — One box, then many: offline federation

*Goal: NightShift scales across a company's sites without ever
becoming a cloud product.*

- **LAN/Tailscale sync:** boxes at different sites exchange briefs,
  learned house rules, and playbooks peer-to-peer over the local
  network or the owner's own tailnet — signed, encrypted, and
  delay-tolerant (sync when a link exists, never require one).
- **Fleet tooling, offline:** the ProdForge catalog and its vetting
  pipeline (mcpaudit/mcpvet) ship as a local bundle, so new MCP tools
  are audited and adopted on-prem with the same PASS/WARN/FAIL bar —
  the fleet discipline we ran at the hackathon, productized.
- **Role specialization:** with several boxes, nights split by
  domain (support box, infra box) with a shared morning roll-up —
  still one approval queue, still one human in charge.

**Acceptance:** two boxes, no internet, one shared simulated company:
rules learned at site A measurably improve drafts at site B after a
sync, and a week fully disconnected loses nothing.

---

## The through-line

Phase 0 proved the night can be worked. Phases 1–2 make NightShift a
*resident* — alive, self-maintaining, keeping its own hours. Phases
3–4 make it a *colleague* — careful, self-doubting, learning the
house. Phases 5–6 make it *trusted* — autonomy that is earned in
public, measured in receipts, and revocable in one command. At every
phase the deal is the same as today's: an uncensored local mind inside
a gated, auditable system — private by architecture, not by promise.
