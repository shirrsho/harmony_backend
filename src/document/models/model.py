from pydantic import BaseModel

class Document(BaseModel):
    project_id: str
    title: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "project_id",
                    "title": "Foo!",
                }
            ]
        }
    }