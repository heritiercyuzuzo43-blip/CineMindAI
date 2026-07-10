import sys
from pathlib import Path
import json
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import LabelEncoder

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATA_PATH, MODEL_PATH, ENCODER_PATH, MODEL_METRICS_PATH, FEATURE_COLUMNS, TARGET_COLUMN
from src.data_preprocessing import prepare_data
from src.utils import ensure_directories, load_dataset


def build_pipeline(classifier):
    categorical_features = ["genre"]
    numeric_features = ["budget", "runtime", "release_month", "popularity_score"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))]), categorical_features),
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_features),
        ]
    )

    return Pipeline([("preprocessor", preprocessor), ("classifier", classifier)])


def train_models():
    ensure_directories()
    df = load_dataset(DATA_PATH)
    X_train, X_test, y_train, y_test = prepare_data(df)

    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    results = {}
    trained_models = {}
    for name, classifier in models.items():
        pipeline = build_pipeline(classifier)
        pipeline.fit(X_train, y_train_encoded)
        pred = pipeline.predict(X_test)
        trained_models[name] = pipeline
        results[name] = {
            "accuracy": accuracy_score(y_test_encoded, pred),
            "precision": precision_score(y_test_encoded, pred, average="weighted", zero_division=0),
            "recall": recall_score(y_test_encoded, pred, average="weighted", zero_division=0),
            "f1": f1_score(y_test_encoded, pred, average="weighted", zero_division=0),
            "confusion": confusion_matrix(y_test_encoded, pred),
        }

    best_model_name = max(results, key=lambda k: results[k]["f1"])
    best_model = trained_models[best_model_name]
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(label_encoder, ENCODER_PATH)

    metrics_payload = {
        "selected_model": best_model_name,
        "class_labels": ["Hit", "Average", "Flop"],
        "training_summary": {
            "training_samples": len(X_train),
            "testing_samples": len(X_test),
            "features_used": FEATURE_COLUMNS,
            "target_variable": TARGET_COLUMN,
            "classes": ["Hit", "Average", "Flop"],
            "selected_algorithm": best_model_name,
            "evaluation_metric": "F1 Score",
        },
        "models": {},
    }

    for name, metrics in results.items():
        metrics_payload["models"][name] = {
            "accuracy": float(metrics["accuracy"]),
            "precision": float(metrics["precision"]),
            "recall": float(metrics["recall"]),
            "f1_score": float(metrics["f1"]),
            "confusion_matrix": metrics["confusion"].tolist(),
            "classification_report": classification_report(
                y_test_encoded,
                trained_models[name].predict(X_test),
                target_names=label_encoder.inverse_transform(label_encoder.classes_),
                output_dict=True,
            ),
        }

    metrics_path = Path(MODEL_METRICS_PATH)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    print("Model training completed")
    for name, model_metrics in metrics_payload["models"].items():
        print(name, model_metrics)
    print("Best model:", best_model_name)


if __name__ == "__main__":
    train_models()
