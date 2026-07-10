import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from src.config import FEATURE_COLUMNS, TARGET_COLUMN


def create_label(row):
    if row["revenue"] >= 150_000_000:
        return "Hit"
    if row["revenue"] >= 60_000_000:
        return "Average"
    return "Flop"


def prepare_data(df):
    df = df.copy()
    for column in ["release_month", "popularity_score", "budget", "runtime", "revenue"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df["release_month"] = df["release_month"].fillna(1)
    df["popularity_score"] = df["popularity_score"].fillna(df["popularity_score"].median())
    df["budget"] = df["budget"].fillna(df["budget"].median())
    df["runtime"] = df["runtime"].fillna(df["runtime"].median())
    df["genre"] = df["genre"].fillna("Unknown")

    df[TARGET_COLUMN] = df.apply(create_label, axis=1)
    df = df[["genre", "budget", "runtime", "release_month", "popularity_score", TARGET_COLUMN]].dropna()

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
