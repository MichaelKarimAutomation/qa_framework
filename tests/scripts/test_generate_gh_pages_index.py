"""Unit tests for scripts/generate_gh_pages_index.py."""
from __future__ import annotations

from scripts.generate_gh_pages_index import (
    DISPLAY_NAME_MAP,
    discover_sections,
    render_card,
    render_index_html,
)


def test_discover_sections_excludes_hidden(tmp_path):
    (tmp_path / '.git').mkdir()
    (tmp_path / '.nojekyll').touch()
    (tmp_path / 'allure-suite').mkdir()
    (tmp_path / 'reference').mkdir()
    assert discover_sections(tmp_path) == ['allure-suite', 'reference']


def test_discover_sections_excludes_files(tmp_path):
    (tmp_path / 'allure-suite').mkdir()
    (tmp_path / 'index.html').write_text('x')
    (tmp_path / 'README.md').write_text('x')
    assert discover_sections(tmp_path) == ['allure-suite']


def test_discover_sections_sorted(tmp_path):
    for name in ['zeta', 'alpha', 'mu']:
        (tmp_path / name).mkdir()
    assert discover_sections(tmp_path) == ['alpha', 'mu', 'zeta']


def test_discover_sections_empty(tmp_path):
    assert discover_sections(tmp_path) == []


def test_render_card_uses_friendly_name():
    out = render_card('allure-suite')
    assert 'Test Results' in out
    assert 'href="allure-suite/"' in out
    assert 'auto-discovered' not in out


def test_render_card_marks_unknown_auto_discovered():
    out = render_card('coverage')
    assert 'Coverage' in out
    assert 'auto-discovered' in out
    assert 'href="coverage/"' in out


def test_render_card_title_cases_compound_unknown():
    out = render_card('new-thing_v2')
    assert 'New Thing V2' in out
    assert 'auto-discovered' in out


def test_render_index_html_includes_all_sections():
    html = render_index_html(['allure-suite', 'reference'], '2026-05-19 12:34 UTC')
    assert 'Test Results' in html
    assert 'API Reference' in html
    assert 'href="allure-suite/"' in html
    assert 'href="reference/"' in html
    assert 'Last deployed: 2026-05-19 12:34 UTC' in html


def test_render_index_html_deterministic():
    a = render_index_html(['allure-suite', 'reference'], '2026-05-19 12:34 UTC')
    b = render_index_html(['allure-suite', 'reference'], '2026-05-19 12:34 UTC')
    assert a == b


def test_render_index_html_empty_state():
    html = render_index_html([], '2026-05-19 12:34 UTC')
    assert 'No published subsites' in html
    assert 'Last deployed: 2026-05-19 12:34 UTC' in html


def test_render_index_html_escapes_timestamp():
    html = render_index_html([], '<bad>')
    assert '<bad>' not in html
    assert '&lt;bad&gt;' in html


def test_render_index_html_escapes_section_names():
    # A folder name with HTML-meaningful chars should not break the document.
    html = render_index_html(['weird&name'], '2026-05-19 12:34 UTC')
    assert 'weird&name' not in html  # raw form must be escaped
    assert 'weird&amp;name' in html


def test_render_index_html_is_selfcontained():
    html = render_index_html(['allure-suite'], '2026-05-19 12:34 UTC')
    assert '<script' not in html.lower()
    assert 'http://' not in html
    assert 'https://' not in html
    assert '<link' not in html.lower()


def test_known_mapping_has_expected_entries():
    assert DISPLAY_NAME_MAP['allure-suite'] == 'Test Results'
    assert DISPLAY_NAME_MAP['reference'] == 'API Reference'


def test_main_writes_file(tmp_path, capsys):
    from scripts.generate_gh_pages_index import main
    import sys

    root = tmp_path / 'root'
    root.mkdir()
    (root / 'allure-suite').mkdir()
    (root / 'reference').mkdir()
    out = tmp_path / 'index.html'

    saved_argv = sys.argv
    try:
        sys.argv = [
            'generate_gh_pages_index.py',
            '--root', str(root),
            '--output', str(out),
            '--timestamp', '2026-05-19 12:34 UTC',
        ]
        rc = main()
    finally:
        sys.argv = saved_argv

    assert rc == 0
    assert out.is_file()
    content = out.read_text(encoding='utf-8')
    assert 'Test Results' in content
    assert 'API Reference' in content
    assert 'Last deployed: 2026-05-19 12:34 UTC' in content
