from fastapi import APIRouter
from src.endpoints import project, srs, conflict

router = APIRouter()
router.include_router(project.router)
router.include_router(srs.router)
router.include_router(conflict.router)