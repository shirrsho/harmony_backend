from fastapi import HTTPException
from src.project.models.model import SRSProject

def validateProject(project: SRSProject):
    if not project.project_title:
        raise HTTPException(status_code=400, detail="Project Title cannot be empty", headers={"X-Error": "Title cannot be empty."})