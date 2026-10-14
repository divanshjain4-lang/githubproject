from typing import Annotated

from pydantic import BaseModel, Field


class SegmentationRequest(BaseModel):
    customer_id: Annotated[str, Field(min_length=1, max_length=128)]
    account_type: Annotated[str, Field(min_length=1, max_length=100)]
    product_codes: list[str] = Field(default_factory=list, max_length=30)
    relationship_tenure_months: int | None = Field(default=None, ge=0, le=1_200)
    interaction_text: str | None = Field(default=None, max_length=5_000)


class BatchSegmentationRequest(BaseModel):
    customers: list[SegmentationRequest] = Field(min_length=1, max_length=1_000)


class SegmentationResponse(BaseModel):
    customer_id: str
    segment: str
    confidence: float = Field(ge=0, le=1)
    rationale: list[str]
    model_version: str
    scoring_mode: str


class TrainingRequest(BaseModel):
    dataset_path: str = Field(default="data/sample/customers.csv", min_length=1)


class TrainingResponse(BaseModel):
    model_version: str
    training_rows: int
    accuracy: float
    labels: list[str]
