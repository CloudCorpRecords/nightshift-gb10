"""Watcher agent — ingests the night's work into a common Item shape.

Demo sources are local JSON exports in data/sample/ (inbox, tickets, CRM,
incidents). In production these become real local-network collectors; the
Item contract below is what the rest of the pipeline depends on.

Item shape (core fields):
  {id, source, time, author, subject, body, topic, thread_id, priority, meta}

Core fields are always present; optional fields (thread_id, priority, meta)
are passed through when present in the source export.
"""
import json
import time
from pathlib import Path

SOURCES = ("inbox", "tickets", "crm", "incidents")

# Fields the rest of the pipeline depends on (the contract)
CORE_FIELDS = {"id", "source", "time", "author", "subject", "body", "topic"}


def night_key(hhmm):
    """Sort key for an overnight window: times before noon belong to the
    next day (the night starts in the evening)."""
    try:
        h, m = (int(x) for x in hhmm.split(":"))
    except Exception:
        return 0
    return h * 60 + m + (1440 if h < 12 else 0)


def _item(raw, source):
    """Build a unified Item from a raw export row. Core fields are always
    present; optional fields (thread_id, priority, meta) pass through."""
    item = {
        "id": raw["id"],
        "source": source,
        "time": raw.get("time", ""),
        "author": raw.get("author", "unknown"),
        "subject": raw.get("subject", "(no subject)"),
        "body": raw.get("body", ""),
        "topic": raw.get("topic", "general"),
    }
    # Pass through optional enrichment fields
    for key in ("thread_id", "priority", "status", "assignee"):
        if key in raw:
            item[key] = raw[key]
    # Capture any extra fields in meta for audit trail
    extra = {k: v for k, v in raw.items()
             if k not in CORE_FIELDS and k not in item}
    if extra:
        item["meta"] = extra
    return item


def load_items(data_dir):
    data_dir = Path(data_dir)
    items = []
    for source in SOURCES:
        path = data_dir / f"{source}.json"
        if not path.exists():
            continue
        for raw in json.loads(path.read_text()):
            items.append(_item(raw, source))
    items.sort(key=lambda i: night_key(i["time"]))
    return items


def load_incoming(incoming_dir):
    """Scan data/incoming/ for new JSON exports and ingest them as Items.

    Each file should contain a JSON array of raw export rows. The filename
    determines the source (e.g. inbox.json → source "inbox"). Files are
    consumed (moved to data/incoming/.processed/) after ingestion so they
    aren't picked up twice during a live demo.

    Returns a list of newly ingested Items (empty if no new files).
    """
    incoming_dir = Path(incoming_dir)
    if not incoming_dir.exists():
        return []

    processed = incoming_dir / ".processed"
    processed.mkdir(exist_ok=True)

    items = []
    for path in sorted(incoming_dir.glob("*.json")):
        try:
            source = path.stem  # e.g. "inbox" from "inbox.json"
            raw_list = json.loads(path.read_text())
            for raw in raw_list:
                items.append(_item(raw, source))
            # Mark consumed
            dest = processed / f"{path.stem}_{int(time.time())}.json"
            path.rename(dest)
        except Exception:
            # Don't let a bad file break the demo — skip and log
            continue

    return items
