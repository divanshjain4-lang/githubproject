# Bank Muscat BRD — Customer Segmentation by Account Type

An API-first foundation for segmenting banking customers from account attributes and (optionally) customer text such as relationship-manager notes or service requests.

## Current scope

- Rule-based account-type segmentation suitable for early BRD validation
- NLP classification with TF-IDF + logistic regression when a labeled training data set is available
- FastAPI contract for individual and batch scoring
- No customer data, credentials, or production model artifacts are stored in this repository

## Run locally (Windows)

```powershell
.\setup.ps1
.\run.ps1
```

The first run trains a local demo model from `data/sample/customers.csv`, then starts the application at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for interactive API documentation.

To stop it, press `Ctrl+C` in the same PowerShell window.

## Train with approved data

Your CSV must contain `account_type`, `product_codes`, `relationship_tenure_months`, `interaction_text`, and the approved target label `segment`.

```powershell
.\.venv\Scripts\python.exe -m app.cli train --data "C:\path\to\approved_data.csv"
```

The resulting local model is stored under `models/` and is excluded from version control. Until a model exists, the API automatically uses transparent account-type rules.

## BRD review checklist

Before model training or deployment, confirm the approved definitions for account types, required input fields, data-retention rules, PII handling, model explainability, acceptance thresholds, and human-review workflow. Update `app/core/segmentation_rules.py` with the signed-off business rules. The included sample data is synthetic and must not be treated as Bank Muscat data or business policy.

## Example request

```json
{
  "customer_id": "CUST-1001",
  "account_type": "Savings",
  "product_codes": ["SAV", "DEBIT"],
  "relationship_tenure_months": 18,
  "interaction_text": "Customer prefers digital banking and uses a debit card frequently."
}
```
