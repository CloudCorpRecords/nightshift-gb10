"""Briefer agent — renders the morning brief + the approval queue.

The brief is the product's main interface: what happened, what matters,
what's drafted, what needs a human decision. It is written twice from one
model: `morning-brief.md` (terminal / git / phone) and `morning-brief.html`
(the screen you open at 9am). The queue is machine-readable so the approval
gate (orchestrator.approve) executes exactly what was shown.

Stdlib only. No network. Nothing here can send anything.
"""
import html as _html
import json
import os
import platform
from datetime import datetime
from pathlib import Path

from .watchers import night_key

# A local doc is cited only when its retrieval quality score meets the
# threshold. Weaker matches are noise the human shouldn't read.
from .research import MIN_QUALITY

TOPIC_LABEL = {"incident": "Incident", "billing": "Billing", "support": "Support",
               "sales": "Sales", "crm-hygiene": "CRM hygiene", "general": "General",
               "noise": "Noise"}
SOURCE_ORDER = ("inbox", "tickets", "crm", "incidents")
APPROVE_ALL = "python3 -m src.nightshift.main approve --all"
APPROVE_IDS = "python3 -m src.nightshift.main approve --ids"


# ---------------------------------------------------------------- model --

def _strong(findings):
    return [f for f in findings
            if f.get("quality", 0) >= MIN_QUALITY or f.get("hits", 0) >= 3]


def _label(topic):
    return TOPIC_LABEL.get(topic, topic.title())


def _n(count, word):
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def _window(items):
    if not items:
        return ""
    ordered = sorted(items, key=lambda i: night_key(i["time"]))
    return f"{ordered[0]['time']} → {ordered[-1]['time']}"


def _model_label():
    url = os.environ.get("NIGHTSHIFT_MODEL_URL", "").strip()
    return f"local model at {url}" if url else "deterministic drafter, no model loaded"


def build(clusters_with_drafts):
    """Turn the orchestrator's entries into one brief model shared by every renderer."""
    items = [i for e in clusters_with_drafts for i in e["cluster"]["items"]]
    counts = {s: sum(1 for i in items if i["source"] == s) for s in SOURCE_ORDER}
    sections, queue = [], []
    for n, entry in enumerate(clusters_with_drafts, 1):
        c, draft = entry["cluster"], entry["draft"]
        findings = _strong(entry["findings"])
        qid = f"Q{n}" if c["topic"] != "noise" else None
        sections.append({
            "n": n, "qid": qid, "topic": c["topic"], "label": _label(c["topic"]),
            "urgency": c["urgency"], "items": c["items"], "findings": findings,
            "draft": draft, "headline": c["items"][0]["subject"],
            "red_flags": list(c.get("red_flags") or []),
        })
        if qid:
            queue.append({"queue_id": qid, "topic": c["topic"], "kind": draft["kind"],
                          "text": draft["text"], "sources": draft["sources"],
                          "status": "pending"})
    now = datetime.now()
    return {
        "generated": now.strftime("%Y-%m-%d %H:%M"),
        "host": platform.node() or "this machine",
        "model": _model_label(),
        "window": _window(items),
        "counts": counts, "items": len(items),
        "clusters": len(sections), "queued": len(queue), "sent": 0,
        "sections": sections, "queue": queue,
        "top": [s for s in sections if s["qid"]][:3],
        "flagged": [s for s in sections if s["red_flags"]],
    }


# ------------------------------------------------------------- markdown --

def _bar(urgency):
    filled = max(0, min(10, round(urgency / 10)))
    return "█" * filled + "░" * (10 - filled)


def render_markdown(b):
    L = []
    L += ["# Morning Brief — NightShift", "",
          f"Night window {b['window']} · generated {b['generated']} on `{b['host']}` · "
          f"{b['model']}", "",
          "> **Nothing was sent overnight.** Every item below is a draft waiting for "
          "your approval. Approving executes against local systems and writes a receipt.",
          ""]
    if b["flagged"]:
        L += ["## 🚩 Red flags, read these first", "",
              "_Churn, legal, breach or money-back language. Rank order is unchanged; "
              "this is visibility, not reordering._", ""]
        for s in b["flagged"]:
            i = s["items"][0]
            L.append(f"- **{s['qid'] or s['label']} · {s['label']}** ({', '.join(s['red_flags'])}) — "
                     f"{i['author']}: {i['subject']}")
        L.append("")
    src_summary = " · ".join(f"{b['counts'][s]} {s}" for s in SOURCE_ORDER if b['counts'][s])
    L += ["## At a glance", "",
          "| | |", "|---|---|",
          f"| Items ingested | {b['items']} ({src_summary}) |",
          f"| Clusters | {b['clusters']} |",
          f"| Drafts queued | {b['queued']} |",
          f"| Sent | {b['sent']} |", ""]
    if b["top"]:
        L += ["**Needs you first**", ""]
        for s in b["top"]:
            why = f", playbook `{s['findings'][0]['doc']}`" if s["findings"] else ""
            L.append(f"{s['n']}. **{s['qid']} · {s['label']} · {s['urgency']}/100** — "
                     f"{s['headline']} ({_n(len(s['items']), 'item')}{why})")
        L.append("")
    L += ["## Approval queue", "",
          "| Queue | Urgency | Topic | Draft | Sources |", "|---|---|---|---|---|"]
    for s in b["sections"]:
        if s["qid"]:
            flag = " 🚩" if s["red_flags"] else ""
            L.append(f"| {s['qid']} | `{_bar(s['urgency'])}` {s['urgency']} | {s['label']}{flag} | "
                     f"{s['draft']['kind']} | {len(s['items'])} |")
    L += ["", f"Approve everything: `{APPROVE_ALL}`  ",
          f"Approve a selection: `{APPROVE_IDS} Q1 Q2`", ""]
    noise = []
    for s in b["sections"]:
        if not s["qid"]:
            noise.append(s)
            continue
        flag = f" · 🚩 {', '.join(s['red_flags'])}" if s["red_flags"] else ""
        L += [f"## {s['n']} · {s['label']} · {s['qid']} · urgency {s['urgency']}/100 · "
              f"{_n(len(s['items']), 'item')}{flag}", "", "**What happened**", ""]
        for i in s["items"]:
            L.append(f"- {i['time']} · {i['source']} · {i['author']}: {i['subject']}")
        L.append("")
        if s["findings"]:
            L += ["**From our docs** (local retrieval only)", ""]
            for f in s["findings"]:
                L.append(f"- `{f['doc']}`: {f['line'].lstrip('- ').strip()}")
            L.append("")
        L += [f"**Draft · {s['draft']['kind']}**", "", f"> {s['draft']['text']}", "",
              f"Approve this one: `{APPROVE_IDS} {s['qid']}`", "", "---", ""]
    if noise:
        L += ["## Filed as noise (no action)", ""]
        for s in noise:
            for i in s["items"]:
                L.append(f"- {i['time']} · {i['source']} · {i['author']}: {i['subject']}")
        L.append("")
    L += [f"_Receipts: `outputs/receipts.log`. Local only: no cloud API anywhere in this "
          f"pipeline. Sent overnight: {b['sent']}._", ""]
    return "\n".join(L)


# ----------------------------------------------------------------- html --

CSS = """
:root{--bg:#0b1020;--card:#141a2e;--line:#242c45;--text:#e6e9f2;--muted:#9aa3b8;
--accent:#f5b942;--hi:#ff5d5d;--mid:#f5b942;--lo:#4cc9b0;--mono:ui-monospace,SFMono-Regular,
Menlo,Consolas,monospace}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);
font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:40px 24px 64px}
header h1{font-size:34px;margin:0 0 6px;letter-spacing:-.02em}
header .sub{color:var(--muted);font-size:14px}
.gate{margin:22px 0 0;padding:14px 18px;border:1px solid var(--accent);border-radius:10px;
background:rgba(245,185,66,.08)}
.gate b{color:var(--accent)}
.flags{margin:14px 0 0;padding:14px 18px;border:1px solid var(--hi);border-radius:10px;
background:rgba(255,93,93,.08)}
.flags b{color:var(--hi)}.flags ul{margin:8px 0 0;padding-left:20px}.flags li{margin:4px 0}
.badge{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
color:var(--hi);border:1px solid var(--hi);border-radius:999px;padding:1px 8px;margin-left:8px;vertical-align:middle}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:28px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.card .k{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.08em}
.card .v{font-size:30px;font-weight:650;margin-top:4px;letter-spacing:-.02em}
.card .d{color:var(--muted);font-size:12px;margin-top:2px}
h2{font-size:14px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:36px 0 12px}
ol.top{margin:0;padding-left:22px}ol.top li{margin:6px 0}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);
border-radius:12px;overflow:hidden}
th,td{text-align:left;padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:middle}
th{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.08em}
tr:last-child td{border-bottom:0}
.bar{display:inline-block;width:90px;height:8px;background:var(--line);border-radius:4px;
vertical-align:middle;margin-right:8px;overflow:hidden}
.bar i{display:block;height:100%}
.q{font-family:var(--mono);font-weight:600;color:var(--accent)}
code,pre{font-family:var(--mono);font-size:13px;background:#0f1528;border:1px solid var(--line);
border-radius:6px;padding:2px 6px}
pre{padding:12px 14px;overflow:auto}
section.cl{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 24px;
margin:16px 0;border-left:4px solid var(--lo)}
section.cl.hi{border-left-color:var(--hi)}section.cl.mid{border-left-color:var(--mid)}
section.cl h3{margin:0 0 4px;font-size:20px;letter-spacing:-.01em}
section.cl .meta{color:var(--muted);font-size:13px;margin-bottom:14px}
.lbl{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:14px 0 6px}
ul.tl{list-style:none;margin:0;padding:0}ul.tl li{padding:4px 0;border-bottom:1px dashed var(--line)}
ul.tl li:last-child{border-bottom:0}ul.tl .t{font-family:var(--mono);color:var(--accent);margin-right:8px}
ul.tl .s{color:var(--muted);margin-right:8px}
.doc{color:var(--muted)}.doc code{color:var(--lo)}
.draft{margin:8px 0 0;padding:14px 16px;background:#0f1528;border:1px solid var(--line);
border-radius:10px;border-left:3px solid var(--accent)}
.draft .kind{color:var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px}
.approve{margin-top:12px;font-size:13px;color:var(--muted)}
footer{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:16px}
ul.noise{color:var(--muted);margin:0;padding-left:18px}
"""


def _level(u):
    return "hi" if u >= 70 else "mid" if u >= 40 else "lo"


def _color(u):
    return {"hi": "var(--hi)", "mid": "var(--mid)", "lo": "var(--lo)"}[_level(u)]


def render_html(b):
    e = _html.escape
    H = ["<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">",
         "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
         "<title>Morning Brief · NightShift</title>", f"<style>{CSS}</style></head>",
         "<body><div class=\"wrap\"><header>", "<h1>Morning Brief</h1>",
         f"<div class=\"sub\">NightShift · night window {e(b['window'])} · generated "
         f"{e(b['generated'])} on <code>{e(b['host'])}</code> · {e(b['model'])}</div>",
         "<div class=\"gate\"><b>Nothing was sent overnight.</b> Every item below is a draft "
         "waiting for your approval. Approving executes against local systems and writes "
         "a receipt.</div>"]
    if b["flagged"]:
        H.append("<div class=\"flags\"><b>🚩 Red flags, read these first.</b> Churn, legal, breach or "
                 "money-back language. Rank order is unchanged.<ul>")
        for s in b["flagged"]:
            i = s["items"][0]
            H.append(f"<li><span class=\"q\">{e(s['qid'] or s['label'])}</span> · <b>{e(s['label'])}</b> "
                     f"({e(', '.join(s['red_flags']))}) — {e(i['author'])}: {e(i['subject'])}</li>")
        H.append("</ul></div>")
    H.append("</header>")
    src = " · ".join(f"{b['counts'][s]} {s}" for s in SOURCE_ORDER if b['counts'][s])
    H.append("<div class=\"cards\">"
             f"<div class=\"card\"><div class=\"k\">Items ingested</div><div class=\"v\">{b['items']}</div>"
             f"<div class=\"d\">{e(src)}</div></div>"
             f"<div class=\"card\"><div class=\"k\">Clusters</div><div class=\"v\">{b['clusters']}</div>"
             f"<div class=\"d\">duplicates merged, incidents linked</div></div>"
             f"<div class=\"card\"><div class=\"k\">Drafts queued</div><div class=\"v\">{b['queued']}</div>"
             f"<div class=\"d\">waiting for you</div></div>"
             f"<div class=\"card\"><div class=\"k\">Sent</div><div class=\"v\">{b['sent']}</div>"
             f"<div class=\"d\">by design</div></div></div>")
    if b["top"]:
        H.append("<h2>Needs you first</h2><ol class=\"top\">")
        for s in b["top"]:
            why = (f", playbook <code>{e(s['findings'][0]['doc'])}</code>"
                   if s["findings"] else "")
            H.append(f"<li><span class=\"q\">{s['qid']}</span> · <b>{e(s['label'])}</b> · "
                     f"{s['urgency']}/100 — {e(s['headline'])} ({_n(len(s['items']), 'item')}{why})</li>")
        H.append("</ol>")
    H.append("<h2>Approval queue</h2><table><thead><tr><th>Queue</th><th>Urgency</th>"
             "<th>Topic</th><th>Draft</th><th>Sources</th></tr></thead><tbody>")
    for s in b["sections"]:
        if s["qid"]:
            H.append(f"<tr><td class=\"q\">{s['qid']}</td><td><span class=\"bar\"><i style=\"width:"
                     f"{s['urgency']}%;background:{_color(s['urgency'])}\"></i></span>{s['urgency']}</td>"
                     f"<td>{e(s['label'])}{' 🚩' if s['red_flags'] else ''}</td><td>{e(s['draft']['kind'])}</td>"
                     f"<td>{len(s['items'])}</td></tr>")
    H.append("</tbody></table>")
    H.append(f"<pre>{e(APPROVE_ALL)}\n{e(APPROVE_IDS)} Q1 Q2</pre>")
    noise = []
    for s in b["sections"]:
        if not s["qid"]:
            noise.append(s)
            continue
        H.append(f"<section class=\"cl {_level(s['urgency'])}\" id=\"{s['qid']}\">"
                 f"<h3><span class=\"q\">{s['qid']}</span> · {e(s['label'])} · {e(s['headline'])}"
                 + (f"<span class=\"badge\">🚩 {e(', '.join(s['red_flags']))}</span>" if s["red_flags"] else "")
                 + "</h3>"
                 f"<div class=\"meta\">urgency {s['urgency']}/100 · {_n(len(s['items']), 'item')} · "
                 f"{e(_window(s['items']))}</div>")
        H.append("<div class=\"lbl\">What happened</div><ul class=\"tl\">")
        for i in s["items"]:
            H.append(f"<li><span class=\"t\">{e(i['time'])}</span><span class=\"s\">{e(i['source'])} · "
                     f"{e(i['author'])}</span>{e(i['subject'])}</li>")
        H.append("</ul>")
        if s["findings"]:
            H.append("<div class=\"lbl\">From our docs (local retrieval only)</div>")
            for f in s["findings"]:
                H.append(f"<div class=\"doc\"><code>{e(f['doc'])}</code> "
                         f"{e(f['line'].lstrip('- ').strip())}</div>")
        H.append(f"<div class=\"draft\"><div class=\"kind\">Draft · {e(s['draft']['kind'])}</div>"
                 f"{e(s['draft']['text'])}</div>"
                 f"<div class=\"approve\">approve this one: <code>{e(APPROVE_IDS)} {s['qid']}</code></div>"
                 "</section>")
    if noise:
        H.append("<h2>Filed as noise (no action)</h2><ul class=\"noise\">")
        for s in noise:
            for i in s["items"]:
                H.append(f"<li>{e(i['time'])} · {e(i['source'])} · {e(i['author'])}: {e(i['subject'])}</li>")
        H.append("</ul>")
    H.append(f"<footer>Receipts: <code>outputs/receipts.log</code> · Local only: no cloud API "
             f"anywhere in this pipeline · Sent overnight: {b['sent']}</footer></div></body></html>")
    return "\n".join(H)


# --------------------------------------------------------------- render --

def render(clusters_with_drafts, out_dir):
    """Write morning-brief.md, morning-brief.html and approval-queue.json.
    Returns the queue (the contract orchestrator.approve executes against)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    b = build(clusters_with_drafts)
    (out_dir / "morning-brief.md").write_text(render_markdown(b))
    (out_dir / "morning-brief.html").write_text(render_html(b))
    (out_dir / "approval-queue.json").write_text(json.dumps(b["queue"], indent=2))
    return b["queue"]
