from fastapi import APIRouter
from src.conflict.endpoints import routes

router = APIRouter()
router.include_router(routes.router)