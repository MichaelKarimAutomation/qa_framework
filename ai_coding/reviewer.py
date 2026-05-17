#!/usr/bin/env python3
"""
reviewer.py — send a diff to the local model, get verdict, persist, notify.

Hard rules:
  * NEVER call the `ollama` CLI. HTTP API only (PATH-staleness immune).
  * Fail SAFE, never fail open. Missing/malformed VERDICT -> FAIL.
  * Ollama unreachable -> non-zero exit + urgent notify + written record.
"""
from __future__ import annotations
import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"C:\Coding\qa_framework")
ACTIVE = REPO_ROOT / "ai_coding" / "active"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3-coder:30b"
TIMEOUT_SECONDS = 300  # 30b on a 4090 should comfortably finish well under this

SYSTEM_PROMPT = (
    "You are a strict but pragmatic code reviewer. Focus only on real bugs, "
    "correctness defects, security issues, and significant logic problems. "
    "Ignore pure style preferences, formatting, and nitpicks. Be concise. "
    "End your response with EXACTLY one line in this form, with no trailing "
    "text after it:\n"
    "VERDICT: PASS\n"
    "or\n"
    "VERDICT: FAIL"
)


def notify(title: str, message: str, urgent: bool = False) -> None:
    """Desktop notify via plyer. Best-effort — never crash the pipeline."""
    try:
        from plyer import notification  # type: ignore
        notification.notify(
            title=title,
            message=message,
            app_name="qa_framework AI review",
            timeout=20 if urgent else 8,
        )
    except Exception as e:
        # plyer unavailable or no notification backend — log and continue.
        print(f"[notify-fallback] {title}: {message} (plyer error: {e})",
              file=sys.stderr)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Local AI code review via Ollama HTTP API.")
    ap.add_argument("--task", required=True,
                    help="Task folder name under ai_coding/active/<task>/.")
    ap.add_argument("--diff", default=None,
                    help="Path to diff file. Defaults to "
                         "ai_coding/active/<task>/diff.patch.")
    return ap.parse_args()


def call_ollama(diff_text: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": "Review the following diff:\n\n```diff\n" + diff_text + "\n```"},
        ],
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        body = resp.read().decode("utf-8")
        if resp.status != 200:
            raise RuntimeError(f"Ollama returned HTTP {resp.status}: {body[:500]}")
    parsed = json.loads(body)
    content = parsed.get("message", {}).get("content", "")
    if not content.strip():
        raise RuntimeError("Ollama returned empty content.")
    return content


def parse_verdict(text: str) -> str:
    """Return 'PASS' or 'FAIL'. Missing/malformed verdict -> FAIL (safe)."""
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if stripped.upper().startswith("VERDICT:"):
            token = stripped.split(":", 1)[1].strip().upper()
            if token in ("PASS", "FAIL"):
                return token
            return "FAIL"  # malformed verdict
    return "FAIL"  # absent verdict


def write_review(task_dir: Path, body: str, parsing_note: str | None = None) -> None:
    out = task_dir / "review_local.md"
    header = f"# Local AI review — {datetime.now(timezone.utc).isoformat()}\n\n"
    if parsing_note:
        header += f"> PARSING NOTE: {parsing_note}\n\n"
    out.write_text(header + body + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    task_dir = ACTIVE / args.task
    if not task_dir.is_dir():
        print(f"ERROR: task folder does not exist: {task_dir}", file=sys.stderr)
        return 2

    diff_path = Path(args.diff) if args.diff else (task_dir / "diff.patch")
    if not diff_path.is_file():
        print(f"ERROR: diff not found: {diff_path}", file=sys.stderr)
        return 2

    diff_text = diff_path.read_text(encoding="utf-8", errors="replace")
    if not diff_text.strip():
        print("ERROR: diff is empty.", file=sys.stderr)
        return 2

    try:
        review = call_ollama(diff_text)
    except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
        msg = f"Ollama not reachable: {type(e).__name__}: {e}"
        print(msg, file=sys.stderr)
        write_review(task_dir, f"OLLAMA UNREACHABLE\n\n{msg}\n",
                     parsing_note="Review skipped — Ollama call failed.")
        notify("Local review UNAVAILABLE",
               f"Ollama not reachable for task '{args.task}'.", urgent=True)
        return 3
    except Exception as e:
        msg = f"Ollama call failed: {type(e).__name__}: {e}"
        print(msg, file=sys.stderr)
        write_review(task_dir, f"OLLAMA ERROR\n\n{msg}\n",
                     parsing_note="Review failed.")
        notify("Local review FAILED",
               f"Ollama error for task '{args.task}'.", urgent=True)
        return 3

    verdict = parse_verdict(review)
    parsing_note = None
    if not any(ln.strip().upper().startswith("VERDICT:")
               for ln in review.splitlines()):
        parsing_note = ("No VERDICT line found in model output. "
                        "Treating as FAIL (fail-safe).")
    elif verdict == "FAIL" and "VERDICT: FAIL" not in review.upper():
        parsing_note = "Malformed VERDICT line. Treating as FAIL (fail-safe)."

    write_review(task_dir, review, parsing_note=parsing_note)
    print(verdict)
    notify(f"Local review complete — VERDICT: {verdict}",
           f"Task '{args.task}'.", urgent=(verdict != "PASS"))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
