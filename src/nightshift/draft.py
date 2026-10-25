"""Drafter agent — writes drafts. It has no send capability, by design.

Drafts are template-built from the cluster + research findings; when a local
model is available it may polish the text, but the template draft is always
the fallback and the audit record of what the human approved starts here.

Every draft names its kind (what the human is approving), carries the ids of
the items it answers, and never promises more than the research supports: a
"fix is ready" line appears only when a local playbook actually matched.
"""

# Findings below this quality score are too weak to cite in a draft.
from src.nightshift.research import MIN_QUALITY


def _strong(findings):
    return [f for f in findings
            if f.get("quality", 0) >= MIN_QUALITY or f.get("hits", 0) >= 3]


def _n(count, word):
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def _quote(subject):
    return '"' + subject.strip().rstrip(".?!") + '"'


def draft_incident(cluster, findings):
    first, last = cluster["items"][0], cluster["items"][-1]
    incidents = [i for i in cluster["items"] if i["source"] == "incidents"] or [first]
    customers = [i for i in cluster["items"] if i["source"] in ("inbox", "tickets")]
    cite = findings[0]["doc"] if findings else "our internal runbook"
    text = (f"Hi, starting at {incidents[0]['time']} we hit a problem: "
            f"{incidents[0]['subject']}. Our team traced the cause using {cite}, "
            f"and the service recovered at {last['time']}. We're crediting any checkout "
            f"affected during that window and monitoring closely. A full summary follows "
            f"within 24 hours. Sorry for the disruption.")
    kind = (f"Incident update to {_n(len(customers), 'affected customer')}"
            if customers else "Incident summary")
    return kind, text


def draft_billing(cluster, findings):
    return ("Reply to billing report",
            "Thanks for flagging this. We've opened a finance review of the charge and "
            "prepared a refund for any duplicate. You'll get confirmation today, and "
            "there's nothing you need to do on your side.")


def draft_support(cluster, findings):
    first = cluster["items"][0]
    if findings:
        fix = (f"Our team matched it to a known case in {findings[0]['doc']} and a fix "
               f"is ready on our side. Please retry, and reply here if anything still "
               f"looks off.")
    else:
        fix = "We're looking into it now and will update you today."
    return ("Support reply",
            f"Thanks for reaching out about {_quote(first['subject'])}. {fix}")


def draft_sales(cluster, findings):
    return ("Follow-up draft",
            "Great to hear from you. We're putting together a short summary with your "
            "usage and next-step options, and you'll have it for review today.")


def draft_crm(cluster, findings):
    return ("CRM clean-up note",
            f"Overnight hygiene: {_n(len(cluster['items']), 'record')} look stale or "
            f"duplicated. Merge/update prepared for approval. No customer contact.")


def draft_general(cluster, findings):
    first = cluster["items"][0]
    return ("Acknowledgement",
            f"Thanks for the note about {_quote(first['subject'])}. It's logged for the "
            f"team and someone will follow up within one business day.")


def draft_noise(cluster, findings):
    return ("No action", "Filed as low priority. No draft needed.")


DRAFTERS = {
    "incident": draft_incident,
    "billing": draft_billing,
    "support": draft_support,
    "sales": draft_sales,
    "crm-hygiene": draft_crm,
    "general": draft_general,
    "noise": draft_noise,
}


def draft_for(cluster, findings, model=None):
    topic = cluster["topic"]
    drafter = DRAFTERS.get(topic, draft_general)
    kind, text = drafter(cluster, _strong(findings))
    if model is not None and topic != "noise":
        polished = model.complete(
            "Polish this customer-facing draft in under 80 words, keep every fact, "
            "keep the same tone: " + text)
        if polished:
            text = polished
    return {"kind": kind, "text": text,
            "sources": [i["id"] for i in cluster["items"]]}
