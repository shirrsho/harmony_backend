from fastapi import HTTPException
from src.document.models.model import Document

def validateDocument(data: Document):
    if not data.project_id:
        raise HTTPException(status_code=400, detail="No project provided!", headers={"X-Error": "No project provided!"})
    if not data.title:
        raise HTTPException(status_code=400, detail="Document title cannot be empty!", headers={"X-Error": "Document title cannot be empty."})