import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import REPORTS_DIR


def save_prediction_report(input_data, prediction, probabilities):
    report_dir = Path(REPORTS_DIR)
    report_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"prediction_{timestamp}.txt"

    lines = [
        "CineMind AI Prediction Report",
        "=" * 32,
        f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "Input Information",
        "-" * 18,
    ]

    for key, value in input_data.items():
        lines.append(f"{key}: {value}")

    lines.extend([
        "",
        "Prediction Result",
        "-" * 18,
        f"Prediction: {prediction}",
        "Probabilities:",
    ])

    for label, probability in probabilities.items():
        lines.append(f"- {label}: {probability:.2%}")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return str(report_path)
