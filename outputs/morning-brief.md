# Morning Brief — NightShift

Night window 18:42 → 07:30 · generated 2026-10-25 11:51 on `binoapt` · deterministic drafter, no model loaded

> **Nothing was sent overnight.** Every item below is a draft waiting for your approval. Approving executes against local systems and writes a receipt.

## 🚩 Red flags, read these first

_Churn, legal, breach or money-back language. Rank order is unchanged; this is visibility, not reordering._

- **Q2 · Billing** (charged twice) — lee@shopmart.example: Charged twice for March invoice

## At a glance

| | |
|---|---|
| Items ingested | 23 (12 inbox · 6 tickets · 3 crm · 2 incidents) |
| Clusters | 8 |
| Drafts queued | 7 |
| Sent | 0 |

**Needs you first**

1. **Q1 · Incident · 80/100** — payments service 502 spike (7 items, playbook `runbook-payments.md`)
2. **Q2 · Billing · 40/100** — Charged twice for March invoice (3 items, playbook `support-macros.md`)
3. **Q3 · Support · 20/100** — Can't log in since yesterday (4 items, playbook `support-macros.md`)

## Approval queue

| Queue | Urgency | Topic | Draft | Sources |
|---|---|---|---|---|
| Q1 | `████████░░` 80 | Incident | Incident update to 5 affected customers | 7 |
| Q2 | `████░░░░░░` 40 | Billing 🚩 | Reply to billing report | 3 |
| Q3 | `██░░░░░░░░` 20 | Support | Support reply | 4 |
| Q4 | `██░░░░░░░░` 20 | General | Acknowledgement | 1 |
| Q5 | `██░░░░░░░░` 15 | Sales | Follow-up draft | 2 |
| Q6 | `█░░░░░░░░░` 10 | CRM hygiene | CRM clean-up note | 3 |
| Q7 | `█░░░░░░░░░` 10 | General | Acknowledgement | 1 |

Approve everything: `python3 -m src.nightshift.main approve --all`  
Approve a selection: `python3 -m src.nightshift.main approve --ids Q1 Q2`

## 1 · Incident · Q1 · urgency 80/100 · 7 items

**What happened**

- 02:14 · incidents · monitor: payments service 502 spike
- 02:16 · inbox · pat@retailer.example: Checkout failed at payment step
- 02:18 · tickets · retailer.example: Checkout 502 errors
- 02:22 · inbox · jo@boutique.example: Payment page returns 502
- 02:25 · tickets · boutique.example: Payments failing for all orders
- 02:31 · inbox · kim@storefront.example: Urgent: checkout down for our store
- 02:47 · incidents · monitor: payments service recovering

**From our docs** (local retrieval only)

- `runbook-payments.md`: Symptom: payments service returns 502 errors at checkout; error rate spikes above 5%.

**Draft · Incident update to 5 affected customers**

> Hi, starting at 02:14 we hit a problem: payments service 502 spike. Our team traced the cause using runbook-payments.md, and the service recovered at 02:47. We're crediting any checkout affected during that window and monitoring closely. A full summary follows within 24 hours. Sorry for the disruption.

Approve this one: `python3 -m src.nightshift.main approve --ids Q1`

---

## 2 · Billing · Q2 · urgency 40/100 · 3 items · 🚩 charged twice

**What happened**

- 21:03 · inbox · lee@shopmart.example: Charged twice for March invoice
- 21:10 · tickets · shopmart.example: Duplicate charge on invoice
- 05:20 · inbox · ops@foodchain.example: Invoice copy for April?

**From our docs** (local retrieval only)

- `support-macros.md`: Duplicate charge: queue a finance review and draft a refund for the duplicate; confirm to the customer the same day.

**Draft · Reply to billing report**

> Thanks for flagging this. We've opened a finance review of the charge and prepared a refund for any duplicate. You'll get confirmation today, and there's nothing you need to do on your side.

Approve this one: `python3 -m src.nightshift.main approve --ids Q2`

---

## 3 · Support · Q3 · urgency 20/100 · 4 items

**What happened**

- 20:17 · inbox · sam@brightco.example: Can't log in since yesterday
- 20:30 · tickets · brightco.example: Login loop — 2 users
- 03:10 · inbox · sam@brightco.example: Still locked out (login loop)
- 03:12 · tickets · brightco.example: Login loop (duplicate of T3)

**From our docs** (local retrieval only)

- `support-macros.md`: Login loop: usually a stale SSO session cookie. Ask the user to clear cookies for our domain and retry; if two or more users at one company are affected, check the company's SSO config before replying.

**Draft · Support reply**

> Thanks for reaching out about "Can't log in since yesterday". Our team matched it to a known case in support-macros.md and a fix is ready on our side. Please retry, and reply here if anything still looks off.

Approve this one: `python3 -m src.nightshift.main approve --ids Q3`

---

## 4 · General · Q4 · urgency 20/100 · 1 item

**What happened**

- 05:40 · tickets · maker.example: Feature request: export to CSV

**Draft · Acknowledgement**

> Thanks for the note about "Feature request: export to CSV". It's logged for the team and someone will follow up within one business day.

Approve this one: `python3 -m src.nightshift.main approve --ids Q4`

---

## 5 · Sales · Q5 · urgency 15/100 · 2 items

**What happened**

- 18:42 · inbox · dana@acme.example: Renewal — expanding to 40 seats?
- 06:05 · inbox · it@lawfirm.example: Demo request — 15-person firm

**Draft · Follow-up draft**

> Great to hear from you. We're putting together a short summary with your usage and next-step options, and you'll have it for review today.

Approve this one: `python3 -m src.nightshift.main approve --ids Q5`

---

## 6 · CRM hygiene · Q6 · urgency 10/100 · 3 items

**What happened**

- 01:00 · crm · crm-export: Stale contact: no activity 180 days
- 01:00 · crm · crm-export: Duplicate company record: Acme / Acme Inc
- 01:00 · crm · crm-export: Account with no owner

**From our docs** (local retrieval only)

- `crm-hygiene.md`: Duplicate company records: merge into the record with the longer history; never delete the merged history.

**Draft · CRM clean-up note**

> Overnight hygiene: 3 records look stale or duplicated. Merge/update prepared for approval. No customer contact.

Approve this one: `python3 -m src.nightshift.main approve --ids Q6`

---

## 7 · General · Q7 · urgency 10/100 · 1 item

**What happened**

- 04:45 · inbox · founder@tinyagency.example: Partnership idea

**Draft · Acknowledgement**

> Thanks for the note about "Partnership idea". It's logged for the team and someone will follow up within one business day.

Approve this one: `python3 -m src.nightshift.main approve --ids Q7`

---

## Filed as noise (no action)

- 19:05 · inbox · newsletter@devweekly.example: This week in dev tools
- 07:30 · inbox · events@conf.example: Last chance: booth discount!!!

_Receipts: `outputs/receipts.log`. Local only: no cloud API anywhere in this pipeline. Sent overnight: 0._
