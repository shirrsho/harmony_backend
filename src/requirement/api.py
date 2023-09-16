from fastapi import APIRouter
from src.requirement.endpoints import routes

router = APIRouter()
router.include_router(routes.router)