"""Researcher agent — answers from PRIVATE LOCAL DOCS only.

Skeleton: keyword retrieval over data/sample/docs/*.md. Each doc is scored by
how many query terms its best line matches; findings carry their source doc
so the brief can cite them. Lane C upgrades this to local embeddings; the
citation contract stays the same.
"""
from pathlib import Path

STOPWORDS = {"about", "after", "again", "every", "first", "since", "their",
             "there", "these", "under", "until", "would", "customer", "customers"}

# A finding is cited only when a doc line matches at least this many query
# terms. Below it, retrieval is guessing — and a brief that cites a guess
# teaches the human to ignore citations. (Raised per BINO's Lane D flag,
# 2026-10-25: brief-side filtering hid the symptom; the threshold belongs
# here, at the source.)
MIN_HITS = 3


def search(docs_dir, query_terms, limit=2, min_hits=MIN_HITS):
    docs_dir = Path(docs_dir)
    scored = []
    if not docs_dir.exists():
        return []
    terms = {t.lower() for t in query_terms} - STOPWORDS
    for doc in sorted(docs_dir.glob("*.md")):
        best_line, best_hits = None, 0
        for line in doc.read_text().splitlines():
            low = line.lower()
            hits = sum(1 for t in terms if t in low)
            if hits > best_hits and line.strip():
                best_line, best_hits = line.strip(), hits
        if best_line and best_hits >= min_hits:
            scored.append({"doc": doc.name, "line": best_line, "hits": best_hits})
    scored.sort(key=lambda f: (-f["hits"], f["doc"]))
    return scored[:limit]


def research(cluster, docs_dir):
    terms = set()
    for item in cluster["items"]:
        for word in (item["subject"] + " " + item["body"]).replace(",", " ").split():
            w = word.strip(".:;()").lower()
            if len(w) > 4:
                terms.add(w)
    if cluster["topic"] == "incident":
        terms.update({"payments", "502", "webhook"})
    return search(docs_dir, sorted(terms))
