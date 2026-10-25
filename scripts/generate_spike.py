"""B3 — Incident log-spike generator for the live demo moment.

Author-Agent: MIKE-SNOOCH
Claim: TASKS #B3, LOG MSG-0030

Usage (demo beat):
  python3 scripts/generate_spike.py --count 6 --time 02:14 --out data/live/incidents.json
  python3 -m src.nightshift.main watch --dir data/live

Output contract matches src/nightshift/watchers.py:
  {id, source, time, author, subject, body, topic}
plus passthrough thread_id / priority (used by watchers.load_incoming).
No secrets, no network, deterministic.
"""
import argparse
import json
from pathlib import Path


def generate_spike(count=6, spike_time="02:14", service="payments"):
    """Return `count` P0 incident items, one per minute from spike_time."""
    items = []
    hh, mm = spike_time.split(":")
    for i in range(count):
        items.append({
            "id": f"S{i+1}",
            "source": "incidents",
            "time": f"{hh}:{int(mm) + i:02d}",
            "author": "monitor",
            "subject": f"{service} service 502 spike",
            "body": (
                f"Error rate {38 + i * 4}% on {service} service; "
                "webhook queue depth rising; suspected webhook queue "
                f"saturation (see runbook). Spike item {i+1}/{count}."
            ),
            "topic": "incident",
            "thread_id": f"{service}-outage",
            "priority": "P0",
        })
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=6)
    ap.add_argument("--time", default="02:14")
    ap.add_argument("--service", default="payments")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    items = generate_spike(args.count, args.time, args.service)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(items, indent=2))
    print(f"Wrote {len(items)} spike items to {out}")


if __name__ == "__main__":
    main()
