from fastapi import APIRouter
from src.project.endpoints import routes

router = APIRouter()
router.include_router(routes.router)