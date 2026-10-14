from fastapi import APIRouter

from app.schemas.customer import (
    BatchSegmentationRequest,
    SegmentationRequest,
    SegmentationResponse,
    TrainingRequest,
    TrainingResponse,
)
from app.services.segmenter import segment_customer
from app.services.model_service import train_model

router = APIRouter()


@router.get("/health", tags=["Operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "customer-segmentation"}


@router.post("/v1/segment", response_model=SegmentationResponse, tags=["Segmentation"])
def segment(request: SegmentationRequest) -> SegmentationResponse:
    return segment_customer(request)


@router.post("/v1/segment/batch", response_model=list[SegmentationResponse], tags=["Segmentation"])
def segment_batch(request: BatchSegmentationRequest) -> list[SegmentationResponse]:
    return [segment_customer(customer) for customer in request.customers]


@router.post("/v1/model/train", response_model=TrainingResponse, tags=["Model administration"])
def train(request: TrainingRequest) -> TrainingResponse:
    """Train a local model from an approved CSV file; never expose this in production without access control."""
    return TrainingResponse(**train_model(request.dataset_path))
