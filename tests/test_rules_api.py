from app.core.segmentation_rules import classify_account_type


def test_unknown_account_type_is_flagged_for_review() -> None:
    result = classify_account_type("New Product", [])
    assert result.segment == "Unclassified Account Type"
    assert result.confidence == 0.40


def test_business_code_takes_precedence() -> None:
    result = classify_account_type("Savings", ["SME"])
    assert result.segment == "Business Banking"
