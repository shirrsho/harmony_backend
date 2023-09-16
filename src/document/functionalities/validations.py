from fastapi import HTTPException
from src.document.models.model import SRSData

def validateDocument(data: SRSData):
    if not data.srs_title:
        raise HTTPException(status_code=400, detail="Document Title cannot be empty!", headers={"X-Error": "Title cannot be empty."})
    if not data.text:
        raise HTTPException(status_code=400, detail="Document content cannot be empty!", headers={"X-Error": "Content cannot be empty."})