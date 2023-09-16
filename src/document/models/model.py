from pydantic import BaseModel
from fastapi import UploadFile

class Document(BaseModel):
    # project_id:str
    project_id: str
    title: str