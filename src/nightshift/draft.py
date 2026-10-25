"""Drafter agent — writes drafts. It has no send capability, by design.

Drafts are template-built from the cluster + research findings; when a local
model is available it may polish the text, but the template draft is always
the fallback and the audit record of what the human approved starts here.
"""

TEMPLATES = {
    "incident": ("Incident update to affected customers",
                 "We're sorry — starting at {first}, we hit a problem: {subject_ref}. "
                 "Our team identified the cause from our internal runbook ({cite}) "
                 "and service is restored. We're crediting affected checkouts and "
                 "monitoring closely. A full summary follows within 24 hours."),
    "billing": ("Reply to billing report",
                "Thanks for flagging this — we've queued a review of the charge and "
                "a refund draft for any duplicate. You'll get confirmation today; "
                "no action needed from you."),
    "support": ("Support reply",
                "Thanks for reaching out about {subject_ref} We've prepared the fix "
                "on our side — please retry, and reply here if anything still looks off."),
    "sales": ("Follow-up draft",
              "Great to hear from you — drafting a renewal summary with usage and "
              "next-step options for your review today."),
    "crm-hygiene": ("CRM clean-up note",
                    "Overnight hygiene: this record looks stale/duplicated. Draft "
                    "merge/update prepared for approval; no customer contact."),
    "noise": ("No action", "Filed as noise/low priority. No draft needed."),
}


def draft_for(cluster, findings, model=None):
    topic = cluster["topic"]
    kind, template = TEMPLATES.get(topic, TEMPLATES["support"])
    first = cluster["items"][0]
    cite = findings[0]["doc"] if findings else "internal notes"
    text = template.format(first=first["time"], subject_ref=first["subject"], cite=cite)
    if model is not None and topic not in ("noise",):
        polished = model.complete(
            "Polish this customer-facing draft in under 80 words, keep every fact: " + text)
        if polished:
            text = polished
    return {"kind": kind, "text": text,
            "sources": [i["id"] for i in cluster["items"]]}
