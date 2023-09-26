from fastapi import APIRouter
from src.project import api as projectapi
from src.document import api as documentapi
from src.conflict import api as conflictapi
from src.requirement import api as requirementapi
from src.report import api as reportapi

router = APIRouter()
router.include_router(projectapi.router)
router.include_router(documentapi.router)
router.include_router(conflictapi.router)
router.include_router(requirementapi.router)
router.include_router(reportapi.router)

@router.get('/')
def get_root():
    return 'Hello from Harmony!'