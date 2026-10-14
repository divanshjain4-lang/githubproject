from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "customer_segment_model.joblib"
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "sample" / "customers.csv"
