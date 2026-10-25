"""Watcher agent — ingests the night's work into a common Item shape.

Demo sources are local JSON exports in data/sample/ (inbox, tickets, CRM,
incidents). In production these become real local-network collectors; the
Item contract below is what the rest of the pipeline depends on.

Item: {id, source, time, author, subject, body, topic}
"""
import json
from pathlib import Path

SOURCES = ("inbox", "tickets", "crm", "incidents")


def night_key(hhmm):
    """Sort key for an overnight window: times before noon belong to the
    next day (the night starts in the evening)."""
    try:
        h, m = (int(x) for x in hhmm.split(":"))
    except Exception:
        return 0
    return h * 60 + m + (1440 if h < 12 else 0)


def load_items(data_dir):
    data_dir = Path(data_dir)
    items = []
    for source in SOURCES:
        path = data_dir / f"{source}.json"
        if not path.exists():
            continue
        for raw in json.loads(path.read_text()):
            items.append({
                "id": raw["id"],
                "source": source,
                "time": raw.get("time", ""),
                "author": raw.get("author", "unknown"),
                "subject": raw.get("subject", "(no subject)"),
                "body": raw.get("body", ""),
                "topic": raw.get("topic", "general"),
            })
    items.sort(key=lambda i: night_key(i["time"]))
    return items
