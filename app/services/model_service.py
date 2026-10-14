"""Local model persistence and training. Intended for approved, de-identified data only."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from app.core.config import MODEL_PATH
from app.schemas.customer import SegmentationRequest

REQUIRED_COLUMNS = {"account_type", "product_codes", "relationship_tenure_months", "interaction_text", "segment"}


def _feature_text(frame: pd.DataFrame) -> pd.Series:
    """Combine structured inputs and free text into a privacy-conscious local NLP feature."""
    prepared = frame.fillna("").copy()
    tenure = pd.to_numeric(prepared["relationship_tenure_months"], errors="coerce").fillna(0).astype(int)
    return (
        "account_type=" + prepared["account_type"].astype(str).str.lower()
        + " products=" + prepared["product_codes"].astype(str).str.lower()
        + " tenure_months=" + tenure.astype(str)
        + " notes=" + prepared["interaction_text"].astype(str).str.lower()
    )


def train_model(dataset_path: str) -> dict[str, object]:
    path = Path(dataset_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.exists():
        raise FileNotFoundError(f"Training data not found: {path}")

    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Training CSV is missing required columns: {', '.join(sorted(missing))}")
    if len(data) < 12 or data["segment"].nunique() < 2:
        raise ValueError("Training data needs at least 12 rows and two segment labels.")

    x = _feature_text(data)
    y = data["segment"].astype(str)
    can_stratify = y.value_counts().min() >= 2
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y if can_stratify else None
    )
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
            ("classifier", LogisticRegression(max_iter=1_000, class_weight="balanced", random_state=42)),
        ]
    )
    pipeline.fit(x_train, y_train)
    accuracy = float(accuracy_score(y_test, pipeline.predict(x_test)))
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    return {
        "model_version": "ml-0.1.0",
        "training_rows": len(data),
        "accuracy": round(accuracy, 4),
        "labels": sorted(y.unique().tolist()),
    }


def predict_with_model(customer: SegmentationRequest) -> tuple[str, float] | None:
    if not MODEL_PATH.exists():
        return None
    pipeline = joblib.load(MODEL_PATH)
    row = pd.DataFrame(
        [
            {
                "account_type": customer.account_type,
                "product_codes": " ".join(customer.product_codes),
                "relationship_tenure_months": customer.relationship_tenure_months or 0,
                "interaction_text": customer.interaction_text or "",
            }
        ]
    )
    features = _feature_text(row)
    probabilities = pipeline.predict_proba(features)[0]
    index = int(probabilities.argmax())
    return str(pipeline.classes_[index]), round(float(probabilities[index]), 4)
