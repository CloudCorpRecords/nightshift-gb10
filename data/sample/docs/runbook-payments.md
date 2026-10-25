# Runbook: Payments Service

- Symptom: payments service returns 502 errors at checkout; error rate spikes above 5%.
- Most common cause: webhook queue saturation — check the webhook queue depth first.
- Fix: drain/restart the webhook queue workers; error rate should fall under 1% within ~30 minutes.
- Customer comms: acknowledge within 1 hour, credit affected checkouts, full summary within 24 hours.
- Escalation: if 502s persist after a queue drain, page the payments on-call lead.
