"""NightShift CLI.

  python3 -m src.nightshift.main run --simulate     # run the simulated night
  python3 -m src.nightshift.main approve --all      # approve the whole queue
  python3 -m src.nightshift.main approve --ids Q1 Q3
  python3 -m src.nightshift.main watch --dir data/live   # live drop-folder mode
"""
import argparse
from pathlib import Path

from .orchestrator import run_night, approve
from .livewatch import watch as live_watch

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(prog="nightshift")
    sub = ap.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run")
    run.add_argument("--simulate", action="store_true",
                     help="use the sample night in data/sample/")
    run.add_argument("--data", default=None)
    run.add_argument("--out", default=str(ROOT / "outputs"))
    app = sub.add_parser("approve")
    app.add_argument("--all", action="store_true")
    app.add_argument("--ids", nargs="*", default=None)
    app.add_argument("--out", default=str(ROOT / "outputs"))
    wat = sub.add_parser("watch")
    wat.add_argument("--dir", default=str(ROOT / "data" / "live"))
    wat.add_argument("--out", default=str(ROOT / "outputs"))
    wat.add_argument("--interval", type=float, default=2.0)
    args = ap.parse_args()

    if args.cmd == "run":
        data_dir = args.data or str(ROOT / "data" / "sample")
        result = run_night(data_dir, str(ROOT / "data" / "sample" / "docs"), args.out)
        print(f"Night complete: {result['items']} items → {result['clusters']} clusters "
              f"→ {result['queued']} drafts queued. Nothing sent.")
        print(f"Brief: {args.out}/morning-brief.md")
    elif args.cmd == "approve":
        ids = None if args.all else (args.ids or [])
        done = approve(args.out, ids=ids)
        print(f"Approved + executed: {', '.join(done) if done else '(none pending)'}")
    elif args.cmd == "watch":
        live_watch(args.dir, args.out, interval=args.interval)


if __name__ == "__main__":
    main()
