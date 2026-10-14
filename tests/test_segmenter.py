from app.schemas.customer import SegmentationRequest
from app.services.segmenter import segment_customer
import pytest


@pytest.fixture(autouse=True)
def use_rules_without_saved_model(monkeypatch):
    monkeypatch.setattr("app.services.segmenter.predict_with_model", lambda customer: None)


def test_savings_customer_is_classified() -> None:
    result = segment_customer(SegmentationRequest(customer_id="C-1", account_type="Savings"))
    assert result.segment == "Retail Savings"
    assert result.confidence == 0.85


def test_business_product_overrides_account_type() -> None:
    result = segment_customer(
        SegmentationRequest(customer_id="C-2", account_type="Current", product_codes=["SME"])
    )
    assert result.segment == "Business Banking"
