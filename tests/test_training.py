import subprocess
import sys

import pytest

from app.core.config import SAMPLE_DATA_PATH
from app.schemas.customer import SegmentationRequest
from app.services import model_service
from app.services.segmenter import segment_customer


def test_training_persistence_and_ml_scoring(tmp_path, monkeypatch):
    monkeypatch.setattr(model_service, "MODEL_PATH", tmp_path / "model.joblib")
    result = model_service.train_model(str(SAMPLE_DATA_PATH))
    assert result["training_rows"] == 32
    assert len(result["labels"]) == 6
    assert 0 <= result["accuracy"] <= 1
    prediction = segment_customer(SegmentationRequest(
        customer_id="TEST-1", account_type="Salary", product_codes=["SAL", "DEBIT"],
        interaction_text="Employer credits salary monthly",
    ))
    assert prediction.scoring_mode == "ml"
    assert prediction.segment == "Payroll Banking"
    assert 0 <= prediction.confidence <= 1


def test_missing_model_uses_rules(tmp_path, monkeypatch):
    monkeypatch.setattr(model_service, "MODEL_PATH", tmp_path / "missing.joblib")
    prediction = segment_customer(SegmentationRequest(customer_id="TEST-2", account_type="Savings"))
    assert prediction.scoring_mode == "rules"
    assert prediction.segment == "Retail Savings"


def test_missing_training_columns(tmp_path):
    dataset = tmp_path / "invalid.csv"
    dataset.write_text("account_type\nSavings\n")
    with pytest.raises(ValueError, match="missing required columns"):
        model_service.train_model(str(dataset))


def test_train_requires_explicit_dataset():
    result = subprocess.run([sys.executable, "-m", "app.cli", "train"], capture_output=True, text=True)
    assert result.returncode == 2
    assert "train requires --data" in result.stderr
