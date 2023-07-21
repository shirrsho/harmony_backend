from pydantic import BaseModel

class SRSData(BaseModel):
    srs_title:str
    text: str