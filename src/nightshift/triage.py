"""Triager agent — clusters related items and scores urgency.

Deterministic by design: the demo (and the audit story) depend on triage the
human can explain. A local model may advise, but the score below is the record.
"""
URGENT_WORDS = ("outage", "down", "502", "failed", "urgent", "charged twice",
                "cancel", "lawsuit", "security", "breach")
TOPIC_BASE = {"incident": 50, "billing": 30, "support": 20, "sales": 15,
              "crm-hygiene": 10, "noise": 0, "general": 10}

# Red flags: business-risk language that must never sit quietly in a queue —
# churn, legal, breach, money-back. Flagged clusters get a callout at the top
# of the brief (rank order unchanged; visibility, not reordering). This is
# also why the model layer runs uncensored (DEC-004): a filter that softens
# "we will cancel" into nothing would hide exactly these items.
RED_FLAG_WORDS = ("cancel", "churn", "lawsuit", "legal action", "breach",
                  "evaluating alternatives", "switching to", "competitor",
                  "charged twice", "refund", "terminate the contract")


def red_flags_for(item):
    text = (item["subject"] + " " + item["body"]).lower()
    return [w for w in RED_FLAG_WORDS if w in text]


def score(item):
    s = TOPIC_BASE.get(item["topic"], 10)
    text = (item["subject"] + " " + item["body"]).lower()
    s += sum(10 for w in URGENT_WORDS if w in text)
    if item["source"] == "incidents":
        s += 20
    return min(s, 100)


def cluster(items):
    """Group items by topic tag (set by exports/watchers). 'general' items are
    kept as singletons (unrelated one-offs) but retain the general topic."""
    from .watchers import night_key
    groups = {}
    for item in items:
        key = item["topic"] if item["topic"] != "general" else f"general:{item['id']}"
        groups.setdefault(key, []).append(item)
    clusters = []
    for key, members in groups.items():
        clusters.append({
            "topic": members[0]["topic"],
            "items": sorted(members, key=lambda i: night_key(i["time"])),
            "urgency": max(score(i) for i in members),
            "red_flags": sorted({w for i in members for w in red_flags_for(i)}),
        })
    clusters.sort(key=lambda c: -c["urgency"])
    return clusters
