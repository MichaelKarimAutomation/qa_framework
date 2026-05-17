"""Generate HTML documentation for the qa-framework Python source.

For each top-level package (pom, utils, data, tests):
  1. Run ``sphinx-apidoc`` to emit per-module .rst files under ``docs/api/``.
  2. Run ``sphinx-build`` once at the end to render the full site to
     ``docs/_build/html/``.

Mirror of the keyword-doc generator batch script in spirit: pick directories,
generate docs for each, render to HTML. Run with ``make docs`` or
``python scripts/generate_docs.py``.

``scripts/`` itself is intentionally excluded — files like delete_reports.py
execute side-effects at import time and would run unwanted commands if
autodoc imported them.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
API_DIR = DOCS / 'api'
BUILD_DIR = DOCS / '_build'
HTML_DIR = BUILD_DIR / 'html'

PACKAGES = ['pom', 'utils', 'data', 'tests', 'performance']
# performance/ requires `autodoc_mock_imports = ['locust']` in docs/conf.py
# to render: Locust monkey-patches gevent/ssl at import time, which would
# trigger RecursionError when imported alongside httpx/urllib3. The mock
# replaces locust during autodoc so the real package is never imported.


def clean() -> None:
    """Wipe previous build output and previously generated .rst stubs so the next run starts from a clean slate."""
    for path in (BUILD_DIR, API_DIR):
        if path.exists():
            shutil.rmtree(path)
            print(f'Cleaned {path.relative_to(ROOT)}')


def generate_api_rst() -> None:
    """Walk each package in PACKAGES and run ``sphinx-apidoc`` to emit one .rst per module under ``docs/api/``."""
    API_DIR.mkdir(parents=True, exist_ok=True)
    for pkg in PACKAGES:
        pkg_path = ROOT / pkg
        if not pkg_path.exists():
            print(f'Skipping {pkg}: directory not found')
            continue
        print(f'Generating .rst stubs for {pkg}/...')
        subprocess.run(
            [
                'sphinx-apidoc',
                '--force',                  # overwrite existing stubs
                '--implicit-namespaces',    # this repo has no __init__.py files
                '--separate',               # one .rst per submodule
                '--no-toc',                 # we provide our own TOC in index.rst
                '-o', str(API_DIR),
                str(pkg_path),
            ],
            check=True,
        )


def generate_makefile_rst() -> None:
    """Parse the project Makefile for ``target: # comment`` lines and the indented shell commands beneath them, then emit ``docs/api/makefile.rst`` so Sphinx renders a browsable Makefile reference."""
    makefile = ROOT / 'Makefile'
    if not makefile.exists():
        print('Skipping Makefile: not found')
        return
    print('Generating .rst for Makefile...')

    target_pattern = re.compile(r'^([\w-]+):[^#]*(?:#\s*(.+))?')
    lines = makefile.read_text().splitlines()

    entries: list[tuple[str, str, list[str]]] = []
    i = 0
    while i < len(lines):
        match = target_pattern.match(lines[i])
        if match:
            target = match.group(1)
            comment = (match.group(2) or '').strip()
            commands: list[str] = []
            j = i + 1
            while j < len(lines) and lines[j].startswith('\t'):
                commands.append(lines[j].strip())
                j += 1
            entries.append((target, comment, commands))
        i += 1

    out = ['Makefile', '========', '',
           'Auto-generated reference for the project ``Makefile``. '
           'Run any target with ``make <target>``.', '']
    for target, comment, commands in entries:
        out.append(f'``make {target}``')
        out.append('-' * (len(target) + 9))
        out.append('')
        if comment:
            out.append(comment)
            out.append('')
        if commands:
            out.append('.. code-block:: shell')
            out.append('')
            for cmd in commands:
                out.append(f'   {cmd}')
            out.append('')

    (API_DIR / 'makefile.rst').write_text('\n'.join(out))


def build_html() -> None:
    """Render the configured Sphinx site (docs/) into ``docs/_build/html/``."""
    print('\nRunning sphinx-build...')
    subprocess.run(
        ['sphinx-build', '-b', 'html', str(DOCS), str(HTML_DIR)],
        check=True,
    )
    print(f'\nDocs ready: {HTML_DIR / "index.html"}')


def main() -> None:
    """Run the full pipeline: clean, generate stubs, render HTML."""
    clean()
    generate_api_rst()
    generate_makefile_rst()
    build_html()


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
