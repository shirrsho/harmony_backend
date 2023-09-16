from pydantic import BaseModel

class Document(BaseModel):
    project_id: str
    title: str