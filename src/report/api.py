from fastapi import APIRouter
from src.report.endpoints import routes

router = APIRouter()
router.include_router(routes.router)