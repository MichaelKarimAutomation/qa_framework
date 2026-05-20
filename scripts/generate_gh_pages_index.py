#!/usr/bin/env python3
"""Generate a root index.html landing page for the gh-pages branch.

Discovers top-level directories on the gh-pages working tree and renders a
self-contained HTML card grid linking to each one. Hidden entries (names
starting with '.') and regular files are skipped. Known directory names are
given friendly labels via DISPLAY_NAME_MAP; unknown directories are rendered
title-cased with an 'auto-discovered' tag so the mapping gap is visible.

The workflow at .github/workflows/gh-pages-index.yml is the only intended
caller; the script is kept importable so the rendering logic can be unit
tested without touching the filesystem of an actual gh-pages checkout.
"""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path

DISPLAY_NAME_MAP: dict[str, str] = {
    'allure-suite': 'Test Results',
    'reference': 'API Reference',
}

PROJECT_NAME = 'qa_framework'
PROJECT_DESCRIPTION = (
    'Published reports and reference documentation for the qa_framework '
    'test automation project.'
)

CSS = """\
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f6f8fa;
  color: #1f2328;
  line-height: 1.5;
}
header {
  background: #24292f;
  color: #fff;
  padding: 2rem 1.5rem;
}
header h1 { margin: 0 0 0.25rem; font-size: 1.75rem; }
header p { margin: 0; opacity: 0.85; }
main {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}
.card {
  background: #fff;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  padding: 1.25rem;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.15s, transform 0.15s;
  display: block;
}
.card:hover {
  border-color: #0969da;
  transform: translateY(-2px);
}
.card h2 { margin: 0 0 0.5rem; font-size: 1.15rem; color: #0969da; }
.card .path {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.85rem;
  color: #57606a;
}
.tag {
  display: inline-block;
  margin-left: 0.5rem;
  padding: 0.1rem 0.4rem;
  background: #fff8c5;
  border: 1px solid #d4a72c;
  border-radius: 3px;
  font-size: 0.7rem;
  color: #57606a;
  vertical-align: middle;
  font-weight: normal;
}
.empty {
  padding: 1.5rem;
  border: 1px dashed #d0d7de;
  border-radius: 6px;
  color: #57606a;
  text-align: center;
}
footer {
  text-align: center;
  padding: 1.5rem;
  color: #57606a;
  font-size: 0.85rem;
}
"""


def discover_sections(root: Path) -> list[str]:
    """Return sorted top-level directory names under *root*, excluding hidden ones."""
    return sorted(
        entry.name
        for entry in root.iterdir()
        if entry.is_dir() and not entry.name.startswith('.')
    )


def _friendly_title(name: str) -> tuple[str, bool]:
    """Return (title, is_known) for a directory name."""
    if name in DISPLAY_NAME_MAP:
        return DISPLAY_NAME_MAP[name], True
    return name.replace('-', ' ').replace('_', ' ').title(), False


def render_card(name: str) -> str:
    title, known = _friendly_title(name)
    tag = '' if known else ' <span class="tag">auto-discovered</span>'
    return (
        f'<a class="card" href="{escape(name)}/">'
        f'<h2>{escape(title)}{tag}</h2>'
        f'<div class="path">{escape(name)}/</div>'
        f'</a>'
    )


def render_index_html(sections: list[str], timestamp: str) -> str:
    if sections:
        body = '<section class="grid">\n      ' + '\n      '.join(
            render_card(name) for name in sections
        ) + '\n    </section>'
    else:
        body = '<div class="empty">No published subsites found yet.</div>'

    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{escape(PROJECT_NAME)}</title>\n'
        '<style>\n'
        f'{CSS}'
        '</style>\n'
        '</head>\n'
        '<body>\n'
        '<header>\n'
        f'  <h1>{escape(PROJECT_NAME)}</h1>\n'
        f'  <p>{escape(PROJECT_DESCRIPTION)}</p>\n'
        '</header>\n'
        '<main>\n'
        f'    {body}\n'
        '</main>\n'
        f'<footer>Last deployed: {escape(timestamp)}</footer>\n'
        '</body>\n'
        '</html>\n'
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True, type=Path,
                    help='Path to the gh-pages working tree root.')
    ap.add_argument('--output', required=True, type=Path,
                    help='Path where index.html should be written.')
    ap.add_argument('--timestamp', required=True,
                    help='Human-readable UTC timestamp for the footer.')
    args = ap.parse_args()

    sections = discover_sections(args.root)
    html = render_index_html(sections, args.timestamp)
    args.output.write_text(html, encoding='utf-8')
    print(f'wrote {args.output} ({len(sections)} section(s))')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
