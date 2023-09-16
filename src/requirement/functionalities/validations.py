from fastapi import HTTPException
from src.requirement.models.model import Requirement

def validateRequirement(requirement: Requirement):
    if not requirement.document_id:
        raise HTTPException(status_code=400, detail="Document ID cannot be empty", headers={"X-Error": "Doc Id cannot be empty."})
    if not requirement.project_id:
        raise HTTPException(status_code=400, detail="Project ID cannot be empty", headers={"X-Error": "Project Id cannot be empty."})
    if not requirement.content:
        raise HTTPException(status_code=400, detail="Content cannot be empty", headers={"X-Error": "Content cannot be empty."})