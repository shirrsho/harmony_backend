from fastapi import APIRouter
from src.endpoints import project, srs

router = APIRouter()
router.include_router(project.router)
router.include_router(srs.router)