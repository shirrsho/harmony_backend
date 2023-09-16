from pydantic import BaseModel
from fastapi import UploadFile

class SRSData(BaseModel):
    # project_id:str
    srs_title:str
    text:str

class SRSFile(BaseModel):
    file:UploadFile