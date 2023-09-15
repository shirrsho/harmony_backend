from fastapi import APIRouter
from src.project import api as projectapi
from src.document import api as documentapi
from src.conflict import api as conflictapi

router = APIRouter()
router.include_router(projectapi.router)
router.include_router(documentapi.router)
router.include_router(conflictapi.router)