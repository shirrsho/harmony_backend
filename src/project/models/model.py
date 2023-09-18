from pydantic import BaseModel

class Project(BaseModel):
    title: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Foo",
                }
            ]
        }
    }