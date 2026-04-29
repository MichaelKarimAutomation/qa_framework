import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
reports = ROOT / "reports"
if reports.exists():
    shutil.rmtree(reports)
    print("Reports folder deleted.")
else:
    print("No ROOT/reports/ found for deletion.")
