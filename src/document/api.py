from fastapi import APIRouter
from src.document.endpoints import routes

router = APIRouter()
router.include_router(routes.router)