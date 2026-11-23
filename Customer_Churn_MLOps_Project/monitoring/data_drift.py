from pathlib import Path
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

ROOT = Path(__file__).resolve().parent.parent
reference_path = ROOT / "data" / "reference.csv"
current_path = ROOT / "data" / "current.csv"

if not reference_path.exists() or not current_path.exists():
    raise FileNotFoundError("Run python src/train.py first to create reference.csv and current.csv.")

reference = pd.read_csv(reference_path)
current = pd.read_csv(current_path)

report = Report([DataDriftPreset()])
snapshot = report.run(reference_data=reference, current_data=current)
out = ROOT / "reports"
out.mkdir(exist_ok=True)
snapshot.save_html(str(out / "data_drift_report.html"))
print(f"Drift report saved to {out / 'data_drift_report.html'}")
