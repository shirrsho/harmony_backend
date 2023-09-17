from pydantic import BaseModel

class Conflict(BaseModel):
    project_id: str
    document_id: str