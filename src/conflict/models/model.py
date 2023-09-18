from pydantic import BaseModel

class Conflict(BaseModel):
    project_id: str
    document_id: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "document_id": "document_id",
                }
            ]
        }
    }