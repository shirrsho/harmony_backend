from pydantic import BaseModel
from fastapi import UploadFile

class SRSProject(BaseModel):
    project_title:str

class SRSData(BaseModel):
    srs_title:str
    text: str

class SRSFile(BaseModel):
    file:UploadFile