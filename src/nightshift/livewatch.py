"""Live watcher (Lane B2) — the "always-on" made visible.

Watches a drop folder. Two kinds of drops:
  * source exports: `inbox.json` / `tickets.json` / `crm.json` /
    `incidents.json` (same arrays the sample night uses), and
  * single items: any `*.item.json` file holding one Item object
    ({id, source, time, author, subject, body, topic}).

On any change it rebuilds the night (brief + approval queue + receipts) into
the out dir. Poll-based on purpose: zero dependencies, works offline on the
GB10, and a human can demo it by dragging a file into the folder.
"""
import json
import shutil
import time
from pathlib import Path

from .orchestrator import run_night
from .watchers import SOURCES

ROOT = Path(__file__).resolve().parents[2]


def _snapshot(watch_dir):
    snap = {}
    for p in sorted(Path(watch_dir).glob("*.json")):
        st = p.stat()
        snap[p.name] = (st.st_mtime_ns, st.st_size)
    return snap


def stage(watch_dir, staging_dir):
    """Merge drops into a run_night-shaped data dir. Returns item count."""
    watch_dir, staging_dir = Path(watch_dir), Path(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)
    merged = {s: [] for s in SOURCES}
    for source in SOURCES:
        src = watch_dir / f"{source}.json"
        if src.exists():
            merged[source].extend(json.loads(src.read_text()))
    for p in sorted(watch_dir.glob("*.item.json")):
        item = json.loads(p.read_text())
        merged.setdefault(item.get("source", "inbox"), []).append(item)
    count = 0
    for source, rows in merged.items():
        (staging_dir / f"{source}.json").write_text(json.dumps(rows))
        count += len(rows)
    return count


def rebuild(watch_dir, staging_dir, docs_dir, out_dir):
    stage(watch_dir, staging_dir)
    return run_night(str(staging_dir), str(docs_dir), str(out_dir))


def watch(watch_dir, out_dir, docs_dir=None, interval=2.0, once=False):
    watch_dir = Path(watch_dir)
    watch_dir.mkdir(parents=True, exist_ok=True)
    docs_dir = docs_dir or str(ROOT / "data" / "sample" / "docs")
    staging = Path(out_dir) / ".live-staging"
    print(f"NightShift live watch → {watch_dir} (drop .json items; Ctrl-C stops)",
          flush=True)
    last = None
    while True:
        snap = _snapshot(watch_dir)
        if snap != last:
            last = snap
            result = rebuild(watch_dir, staging, docs_dir, out_dir)
            stamp = time.strftime("%H:%M:%S")
            print(f"↻ {stamp} — {result['items']} items → {result['clusters']} "
                  f"clusters → {result['queued']} drafts queued. Nothing sent.",
                  flush=True)
            if once:
                return result
        if once:
            return None
        time.sleep(interval)
