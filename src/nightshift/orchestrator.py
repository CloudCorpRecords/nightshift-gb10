"""Orchestrator — runs the night loop and owns the approval gate + receipts.

Invariants enforced here:
- Drafts are never executed without a queue entry a human approved.
- Every execution (and rejection) appends a receipt.
"""
import json
from datetime import datetime
from pathlib import Path

from . import watchers, triage, research, draft as drafter, brief as briefer
from .model import LocalModel


def _receipt(out_dir, msg):
    line = f"{datetime.now().isoformat(timespec='seconds')} · {msg}"
    with open(Path(out_dir) / "receipts.log", "a") as fh:
        fh.write(line + "\n")
    return line


def run_night(data_dir, docs_dir, out_dir, model=None):
    items = watchers.load_items(data_dir)
    clusters = triage.cluster(items)
    model = model if model is not None else LocalModel()
    entries = []
    for c in clusters:
        findings = research.research(c, docs_dir)
        d = drafter.draft_for(c, findings, model=model)
        entries.append({"cluster": c, "findings": findings, "draft": d})
    queue = briefer.render(entries, out_dir)
    _receipt(out_dir, f"night run: {len(items)} items, {len(clusters)} clusters, "
                      f"{len(queue)} drafts queued, 0 sent")
    return {"items": len(items), "clusters": len(clusters), "queued": len(queue)}


# Simulated actions per topic — what "executing" a draft means in demo mode.
# Each entry: (endpoint, target_system, effect_description_template)
_SIMULATED_ACTIONS = {
    "incident": ("POST /api/v1/incidents/postmortem", "status-page",
                 "Published incident summary; credit batch queued for {count} affected merchants"),
    "billing": ("POST /api/v1/billing/review", "billing-system",
                "Queued refund review for {sources}; customer notified"),
    "support": ("POST /api/v1/tickets/{first_source}/reply", "support-desk",
                "Reply sent to thread; ticket status → awaiting-customer"),
    "sales": ("POST /api/v1/crm/opportunity", "crm",
              "Opportunity drafted with next-step template"),
    "crm-hygiene": ("PATCH /api/v1/crm/records", "crm",
                    "Records merged/updated; {count} changes staged for review"),
    "general": ("POST /api/v1/notes", "notes",
                "Acknowledgement note filed"),
}


def _simulate_action(entry):
    """Return a human-readable description of what executing this draft does."""
    topic = entry["topic"]
    sources = entry["sources"]
    action_def = _SIMULATED_ACTIONS.get(topic)
    if not action_def:
        return f"Executed {entry['kind']} (generic)"
    endpoint, system, template = action_def
    first = sources[0] if sources else "unknown"
    desc = template.format(count=len(sources), sources=", ".join(sources),
                           first_source=first)
    return f"[{system}] {endpoint}: {desc}"


def approve(out_dir, ids=None):
    """Execute approved queue items against simulated local systems and mark them
    approved. Each execution writes a detailed receipt with the action taken.
    Returns executed queue ids."""
    out_dir = Path(out_dir)
    queue_path = out_dir / "approval-queue.json"
    queue = json.loads(queue_path.read_text())
    done = []
    for entry in queue:
        if entry["status"] != "pending":
            continue
        if ids is not None and entry["queue_id"] not in ids:
            continue
        entry["status"] = "approved"
        action_desc = _simulate_action(entry)
        entry["executed_action"] = action_desc
        _receipt(out_dir, f"APPROVED {entry['queue_id']} [{entry['topic']}] "
                          f"{entry['kind']} sources={','.join(entry['sources'])} → {action_desc}")
        done.append(entry["queue_id"])
    queue_path.write_text(json.dumps(queue, indent=2))
    return done
