from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI(
    title="Bank Muscat Customer Segmentation API",
    version="0.1.0",
    description="BRD-aligned starter service for account-type customer segmentation.",
)
app.include_router(router)
app.mount("/", StaticFiles(directory=Path(__file__).parent / "web", html=True), name="web")
