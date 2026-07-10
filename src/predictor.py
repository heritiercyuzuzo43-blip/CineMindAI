import sys
from pathlib import Path
import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MODEL_PATH, ENCODER_PATH, FEATURE_COLUMNS


class MoviePredictor:
    def __init__(self, model_path=MODEL_PATH, encoder_path=ENCODER_PATH):
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(encoder_path)

    def predict(self, input_data):
        df = pd.DataFrame([input_data])
        df = df[FEATURE_COLUMNS]
        prediction_encoded = self.model.predict(df)[0]
        probabilities = self.model.predict_proba(df)[0]
        prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
        prob_map = {
            self.label_encoder.inverse_transform([int(cls)])[0]: float(prob)
            for cls, prob in zip(self.model.classes_, probabilities)
        }
        return prediction, prob_map
