#!/usr/bin/env python3
"""
clear_queue.py — archive reviewed clean-pass task folders.

Safety properties (do not weaken):
  * Moves, never deletes.
  * Only PASS-status folders are eligible for age-based archiving.
  * CAP_REACHED / OVERRIDE folders are NEVER auto-moved. They are routed to
    quarantine/ and require an explicit, named manual clear.
  * A missing/unreadable STATUS file is treated as NOT clean -> left in place.

Usage:
  python clear_queue.py --days 7              # age-based, PASS only
  python clear_queue.py --task login-fix      # force-archive one PASS task now
  python clear_queue.py --quarantine login-fix  # explicit manual clear of a
                                                 # flagged folder -> archive
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
QUARANTINE = AI / "quarantine"

CLEAN = {"PASS"}
FLAGGED = {"CAP_REACHED", "OVERRIDE"}


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

    # Explicit manual clear of a flagged folder (the ONLY way flagged moves).
    if args.quarantine:
        td = ACTIVE / args.quarantine
        if not td.is_dir():
            td = QUARANTINE / args.quarantine
        if not td.is_dir():
            print(f"No such task folder: {args.quarantine}")
            return 1
        status = read_status(td)
        print(f"Manually clearing flagged task '{args.quarantine}' (STATUS={status}).")
        move(td, ARCHIVE, args.dry_run)
        return 0

    targets = []
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

        if status in FLAGGED:
            # Route to quarantine; never auto-archive.
            print(f"QUARANTINE: '{td.name}' STATUS={status} "
                  f"(left for manual --quarantine clear).")
            if td.parent != QUARANTINE:
                move(td, QUARANTINE, args.dry_run)
            continue

        if status not in CLEAN:
            print(f"SKIP: '{td.name}' STATUS={status or 'MISSING'} (not clean).")
            continue

        if args.task:  # explicit single-task force (consumption-based path)
            move(td, ARCHIVE, args.dry_run)
            moved += 1
            continue

        if age_days(td) >= args.days:
            move(td, ARCHIVE, args.dry_run)
            moved += 1
        else:
            print(f"KEEP: '{td.name}' clean but younger than {args.days}d.")

    print(f"Done. {moved} folder(s) archived.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Archive reviewed clean-pass task folders.")
    ap.add_argument("--days", type=int, default=7,
                    help="Age threshold for PASS folders (default 7).")
    ap.add_argument("--task", help="Force-archive one PASS task now (consumption-based).")
    ap.add_argument("--quarantine",
                    help="Explicit manual clear of a flagged (CAP_REACHED/OVERRIDE) task.")
    ap.add_argument("--dry-run", action="store_true")
    return run(ap.parse_args())


if __name__ == "__main__":
    sys.exit(main())
