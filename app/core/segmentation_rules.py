"""Interim business rules pending approval of the Bank Muscat BRD."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RuleResult:
    segment: str
    confidence: float
    rationale: list[str]


ACCOUNT_TYPE_SEGMENTS = {
    "savings": "Retail Savings",
    "current": "Retail Transactional",
    "salary": "Payroll Banking",
    "fixed deposit": "Deposits & Investment",
    "term deposit": "Deposits & Investment",
    "business": "Business Banking",
    "corporate": "Corporate Banking",
}


def classify_account_type(account_type: str, product_codes: list[str]) -> RuleResult:
    normalized_type = account_type.strip().casefold()
    segment = ACCOUNT_TYPE_SEGMENTS.get(normalized_type, "Unclassified Account Type")
    rationale = [f"Account type supplied: {account_type.strip()}"]

    if any(code.strip().upper() in {"SME", "BIZ"} for code in product_codes):
        segment = "Business Banking"
        rationale.append("Business product code detected")
        confidence = 0.90
    elif segment == "Unclassified Account Type":
        rationale.append("No approved mapping exists for this account type")
        confidence = 0.40
    else:
        rationale.append("Mapped through interim account-type rule")
        confidence = 0.85

    return RuleResult(segment=segment, confidence=confidence, rationale=rationale)
