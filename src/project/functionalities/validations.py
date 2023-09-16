from fastapi import HTTPException
from src.project.models.model import Project

def validateProject(project: Project):
    if not project.title:
        raise HTTPException(status_code=400, detail="Project Title cannot be empty", headers={"X-Error": "Title cannot be empty."})