from pydantic import BaseModel

class RequirementReport(BaseModel):
    report_id: str
    content: str
    conflicted: list = [
        # {
        #     requirement_id:str,
        #     content:str,
        #     threat:float
        # }
    ]
    mark_as_safe:bool=False

class DocumentReport(BaseModel):
    report_id: str
    title:str
    conflict_count:int=0
    threat:float=0.0
    mark_as_safe:bool=False

class ProjectReport(BaseModel):
    report_id: str
    title:str
    conflict_count:int=0
    threat:float=0.0
    mark_as_safe:bool=False