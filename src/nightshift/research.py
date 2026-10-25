"""Researcher agent — answers from PRIVATE LOCAL DOCS only.

Retrieval over data/sample/docs/*.md using TF-IDF–style scoring: each doc is
scored by how many query terms appear across its lines, weighted by term
rarity across the corpus. Findings carry their source doc, the best-matching
line, and a quality score so the brief can cite with confidence.

The citation contract: a finding is cited only when its quality score meets
the minimum threshold. Below it, retrieval is guessing — and a brief that
cites a guess teaches the human to ignore citations.
"""
import math
from pathlib import Path

STOPWORDS = {"about", "after", "again", "every", "first", "since", "their",
             "there", "these", "under", "until", "would", "customer", "customers",
             "please", "reply", "thanks", "thank", "fixed", "issue", "problem"}

# Quality threshold: findings below this score are not cited.
# Based on term coverage (0–1) × line match strength (0–1).
# Set low enough that relevant docs with partial matches still surface.
MIN_QUALITY = 0.05


def _extract_terms(text):
    """Extract meaningful terms from text, filtering stopwords and short words."""
    terms = set()
    for word in text.replace(",", " ").replace(".", " ").split():
        w = word.strip(".:;()\"'-").lower()
        if len(w) > 3 and w not in STOPWORDS:
            terms.add(w)
    return terms


def _tf_idf_score(doc_lines, query_terms, doc_freqs, total_docs):
    """Score a document using TF-IDF–style weighting.
    
    Returns (quality_score, best_line, term_matches).
    quality_score ∈ [0, 1] based on term coverage and match strength.
    """
    if not query_terms or not doc_lines:
        return 0.0, None, 0

    # Count term occurrences across all lines
    term_counts = {t: 0 for t in query_terms}
    best_line, best_line_score = None, 0

    for line in doc_lines:
        low = line.lower()
        line_score = 0
        for t in query_terms:
            if t in low:
                # IDF weight: rarer terms score higher
                idf = math.log(total_docs / max(doc_freqs.get(t, 1), 1)) + 1
                term_counts[t] += 1
                line_score += idf
        if line_score > best_line_score and line.strip():
            best_line, best_line_score = line.strip(), line_score

    # Coverage: fraction of query terms found in doc
    terms_found = sum(1 for c in term_counts.values() if c > 0)
    coverage = terms_found / len(query_terms) if query_terms else 0

    # Strength: normalized best line score
    max_possible = len(query_terms) * (math.log(total_docs) + 1)
    strength = best_line_score / max_possible if max_possible > 0 else 0

    # Quality = coverage × strength (both ∈ [0, 1])
    quality = coverage * strength

    return quality, best_line, terms_found


def search(docs_dir, query_terms, limit=2, min_quality=MIN_QUALITY):
    """Search local docs for findings matching query terms.
    
    Returns list of findings sorted by quality score, each with:
    - doc: filename
    - line: best matching line
    - quality: score ∈ [0, 1]
    - term_matches: number of query terms found
    """
    docs_dir = Path(docs_dir)
    if not docs_dir.exists():
        return []

    # Load all docs and compute document frequencies
    docs = {}
    for doc in sorted(docs_dir.glob("*.md")):
        lines = [l for l in doc.read_text().splitlines() if l.strip()]
        if lines:
            docs[doc.name] = lines

    if not docs:
        return []

    # Compute document frequencies for IDF
    doc_freqs = {}
    for lines in docs.values():
        all_text = " ".join(lines).lower()
        for t in query_terms:
            if t in all_text:
                doc_freqs[t] = doc_freqs.get(t, 0) + 1

    # Score each document
    scored = []
    for name, lines in docs.items():
        quality, best_line, term_matches = _tf_idf_score(
            lines, query_terms, doc_freqs, len(docs))
        if quality >= min_quality and best_line:
            scored.append({
                "doc": name,
                "line": best_line,
                "quality": round(quality, 3),
                "term_matches": term_matches,
            })

    scored.sort(key=lambda f: (-f["quality"], f["doc"]))
    return scored[:limit]


def research(cluster, docs_dir):
    """Research a cluster of items against local docs."""
    terms = set()
    for item in cluster["items"]:
        terms |= _extract_terms(item["subject"] + " " + item["body"])
    # Topic-specific term boost for incidents
    if cluster["topic"] == "incident":
        terms.update({"payments", "502", "webhook", "checkout", "error"})
    return search(docs_dir, sorted(terms))
