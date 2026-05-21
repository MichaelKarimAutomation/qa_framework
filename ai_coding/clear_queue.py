#!/usr/bin/env python3
"""
clear_queue.py — manual backup utility for archiving task folders.

Primary archival path: `.github/workflows/auto-archive.yml` sweeps
`ai_coding/active/` on every master push and moves task folders whose
STATUS is PASS or OVERRIDE into `ai_coding/archive/`. You should not need
this script in day-to-day use.

This script exists as a backup for when:
  * The auto-archive workflow is broken or unavailable.
  * You want to archive a folder locally before pushing (e.g. clearing
    your active/ dir between sessions on a long-running branch).
  * You want a dry-run preview of what the workflow will move on the
    next master push.

Safety properties (do not weaken):
  * Moves, never deletes.
  * Only PASS / OVERRIDE STATUS folders are eligible.
  * A missing/unreadable STATUS file is treated as NOT eligible → left in place.

Usage:
  python clear_queue.py --days 7              # age-based, eligible folders only
  python clear_queue.py --task login-fix      # force-archive one eligible task now
  python clear_queue.py --days 7 --dry-run
"""
from __future__ import annotations
import argparse
import shutil
import sys
import time
from pathlib import Path

REPO_ROOT = Path(r"C:\Coding\qa_framework")
AI = REPO_ROOT / "ai_coding"
ACTIVE = AI / "active"
ARCHIVE = AI / "archive"

ELIGIBLE = {"PASS", "OVERRIDE"}


def read_status(task_dir: Path) -> str | None:
    f = task_dir / "STATUS"
    try:
        return f.read_text(encoding="utf-8").strip().upper() or None
    except OSError:
        return None


def move(src: Path, dest_parent: Path, dry: bool) -> None:
    dest_parent.mkdir(parents=True, exist_ok=True)
    dest = dest_parent / src.name
    if dest.exists():
        dest = dest_parent / f"{src.name}_{int(time.time())}"
    print(f"{'[dry-run] ' if dry else ''}move {src} -> {dest}")
    if not dry:
        shutil.move(str(src), str(dest))


def age_days(p: Path) -> float:
    return (time.time() - p.stat().st_mtime) / 86400.0


def run(args: argparse.Namespace) -> int:
    if not ACTIVE.exists():
        print(f"No active dir at {ACTIVE}; nothing to do.")
        return 0

    if args.task:
        td = ACTIVE / args.task
        if not td.is_dir():
            print(f"No such active task: {args.task}")
            return 1
        targets = [td]
    else:
        targets = [d for d in ACTIVE.iterdir() if d.is_dir()]

    moved = 0
    for td in targets:
        status = read_status(td)

        if status not in ELIGIBLE:
            print(f"SKIP: '{td.name}' STATUS={status or 'MISSING'} (not eligible).")
            continue

        if args.task:  # explicit single-task force
            move(td, ARCHIVE, args.dry_run)
            moved += 1
            continue

        if age_days(td) >= args.days:
            move(td, ARCHIVE, args.dry_run)
            moved += 1
        else:
            print(f"KEEP: '{td.name}' eligible but younger than {args.days}d.")

    print(f"Done. {moved} folder(s) archived.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Backup utility: archive eligible task folders.")
    ap.add_argument("--days", type=int, default=7,
                    help="Age threshold for eligible folders (default 7).")
    ap.add_argument("--task", help="Force-archive one eligible task now.")
    ap.add_argument("--dry-run", action="store_true")
    return run(ap.parse_args())


if __name__ == "__main__":
    sys.exit(main())
