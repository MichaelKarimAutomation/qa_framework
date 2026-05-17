#!/usr/bin/env python3
"""
notify.py — minimal best-effort desktop notification helper.

Invoked fire-and-forget by .git/hooks/post-commit so the hook never blocks
git and never fails the commit. Failures are logged to stderr only.
"""
from __future__ import annotations
import sys


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: notify.py <title> <message> [urgent]", file=sys.stderr)
        return 2
    title, message = sys.argv[1], sys.argv[2]
    urgent = len(sys.argv) > 3 and sys.argv[3].lower() in ("1", "true", "urgent")
    try:
        from plyer import notification  # type: ignore
        notification.notify(
            title=title,
            message=message,
            app_name="qa_framework AI review",
            timeout=20 if urgent else 8,
        )
    except Exception as e:
        print(f"[notify-fallback] {title}: {message} (plyer error: {e})",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
