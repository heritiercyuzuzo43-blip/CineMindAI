from pathlib import Path
import pandas as pd


def ensure_directories():
    for path in ["data", "models", "reports", "app", "src"]:
        Path(path).mkdir(parents=True, exist_ok=True)


def load_dataset(path):
    return pd.read_csv(path)
