"""NightShift CLI.

  python3 -m src.nightshift.main run --simulate     # run the simulated night
  python3 -m src.nightshift.main approve --all      # approve the whole queue
  python3 -m src.nightshift.main approve --ids Q1 Q3
"""
import argparse
from pathlib import Path

from .orchestrator import run_night, approve

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


if __name__ == "__main__":
    main()
