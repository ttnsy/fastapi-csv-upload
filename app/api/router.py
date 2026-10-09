from fastapi import APIRouter

from app.resources.datasets.analyses.router import router as analyses_router
from app.resources.datasets.router import router as datasets_router

router = APIRouter()

router.include_router(datasets_router)
router.include_router(analyses_router)
