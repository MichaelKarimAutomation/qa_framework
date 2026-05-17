"""Delete the top-level `reports/` directory.

Run from the Makefile or directly between test runs to clear stale Allure
output, Playwright traces, and screenshots so the next run starts from a clean
slate. No-op (with a message) if the folder does not exist.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
reports = ROOT / 'reports'
if reports.exists():
    shutil.rmtree(reports)
    print('Reports folder deleted.')
else:
    print('No ROOT/reports/ found for deletion.')
