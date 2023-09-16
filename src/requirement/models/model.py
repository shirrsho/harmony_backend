from typing import List
from pydantic import BaseModel

class Requirement(BaseModel):
    document_id: str
    project_id: str
    content: str

class RequirementList(BaseModel):
    data:List[Requirement]