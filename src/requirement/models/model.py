from typing import List
from pydantic import BaseModel

class Requirement(BaseModel):
    document_id: str
    project_id: str
    content: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "document_id": "document_id",
                    "project_id": "project_id",
                    "content": "Add requirement!",
                }
            ]
        }
    }

class RequirementList(BaseModel):
    data:List[Requirement]