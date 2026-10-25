#!/usr/bin/env python3
"""Incident generator (B3) — drops realistic incident items into data/live/
with timing that simulates an unfolding outage during the live demo.

Usage:
    python3 scripts/incident-gen.py              # drop all items, 5s apart
    python3 scripts/incident-gen.py --fast       # drop all items, 1s apart
    python3 scripts/incident-gen.py --one LIVE-I1 # drop just one item

Watch NightShift pick them up live:
    python3 -m src.nightshift.main watch --dir data/live
"""
import argparse
import json
import shutil
import time
from pathlib import Path

SEED_DIR = Path(__file__).resolve().parents[1] / "data" / "live-seeds"
LIVE_DIR = Path(__file__).resolve().parents[1] / "data" / "live"

INCIDENT_ITEMS = [
    "incident-spike-1.item.json",   # monitor: error rate 42%
    "incident-spike-2.item.json",   # merchant: checkout down, escalating
    "incident-spike-3.item.json",   # oncall: root cause found, restarting
    "cancel-threat.item.json",       # existing: third outage, will cancel
]


def drop_item(seed_name, live_dir):
    """Copy one seed file into the live directory."""
    src = SEED_DIR / seed_name
    if not src.exists():
        print(f"  ⚠ seed not found: {src}")
        return False
    dest = live_dir / seed_name
    shutil.copy2(src, dest)
    print(f"  ✓ dropped: {seed_name}")
    return True


def main():
    ap = argparse.ArgumentParser(prog="incident-gen")
    ap.add_argument("--fast", action="store_true", help="1s between drops instead of 5s")
    ap.add_argument("--one", default=None, help="Drop only this one seed file")
    ap.add_argument("--dir", default=None, help="Override live directory")
    args = ap.parse_args()

    live_dir = Path(args.dir) if args.dir else LIVE_DIR
    live_dir.mkdir(parents=True, exist_ok=True)
    interval = 1.0 if args.fast else 5.0

    if args.one:
        drop_item(args.one, live_dir)
        print(f"\nDone — 1 item dropped into {live_dir}")
        return

    print(f"Incident generator → {live_dir} ({len(INCIDENT_ITEMS)} items, {interval}s apart)")
    print("Watch NightShift rebuild after each drop:\n")

    for i, seed in enumerate(INCIDENT_ITEMS, 1):
        print(f"[{i}/{len(INCIDENT_ITEMS)}] ", end="", flush=True)
        drop_item(seed, live_dir)
        if i < len(INCIDENT_ITEMS):
            time.sleep(interval)

    print(f"\n✅ Done — {len(INCIDENT_ITEMS)} incident items dropped into {live_dir}")
    print("NightShift should have rebuilt the brief with a new incident cluster.")


if __name__ == "__main__":
    main()
