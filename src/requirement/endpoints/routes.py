from io import BytesIO
from typing import List
from fastapi import APIRouter, HTTPException, Body, File, UploadFile
import pandas as pd
import os
from dotenv import load_dotenv
from mongodb import MongoDB
from src.logger import console_log
from src.requirement.functionalities.operations import addDocumentRequirementstoDB, addRequirementtoDB, deleteRequirement, editRequirement, getDocumentRequirementsFromDB, getProjectRequirementsFromDB, getRequirementFromDB
from src.requirement.functionalities.validations import validateRequirement

from src.requirement.models.model import Requirement, RequirementList
load_dotenv()

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/requirement",
    responses={404: {"description": "Not found"}},
    tags=["Requirement"]
)

@router.post('/', status_code=201)
async def add_requirement(data: Requirement):
    validateRequirement(data)
    try:
        requirement = addRequirementtoDB(data)
        return {
            "message": "Requirement added successfully!",
            "requirement_id": str(requirement.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Requirement cannot be added, Please try again later", headers={"X-Error": str(e)})

# No BaseModel, be careful
@router.post('/document', status_code=201)
async def add_requirements(data: List[dict]):
    # validateRequirement(data)
    # console_log(data)
    try:
        requirements = addDocumentRequirementstoDB(data)
        # return {
        #     "message": "Requirement added successfully!",
        #     "requirement_id": [str(id) for id in requirements.inserted_ids]
        # }
        return [str(id) for id in requirements.inserted_ids]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Requirements cannot be added, Please try again later", headers={"X-Error": str(e)})

@router.post('/{project_id}/{document_id}', status_code=201)
async def upload(project_id:str, document_id:str, file: UploadFile = File(...)):
    # validateRequirement(data)
    # console_log(data)
    try:
        content = await file.read()
        if file.filename.endswith(".csv"):
            try:
                df = pd.read_csv(BytesIO(content))
            except Exception as e:
                console_log(str(e))
        elif file.filename.endswith(".xlsx"):
            try:
                df = pd.read_excel(BytesIO(content))
            except Exception as e:
                console_log(str(e))
            
        else:
            return {"error": "File format not supported"}

        reqs = [{
            'content':r[0],
            'document_id': document_id,
            'project_id':project_id
        } for r in df.__array__()]
        requirements = addDocumentRequirementstoDB(reqs)
        # console_log(reqs)
        return [str(id) for id in requirements.inserted_ids]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Requirements cannot be added, Please try again later", headers={"X-Error": str(e)})

@router.get('/project/{project_id}')
async def get_project_requirements(project_id:str):
    try:
        requirements = getProjectRequirementsFromDB(project_id)
        # return {
        #     "message": "Project requirements are sent successfully",
        #     "requirements": requirements
        # }
        return requirements
    except Exception as e:
        raise HTTPException(status_code=400, detail="Project requirements cannot be fetched, Please try again later", headers={"X-Error": str(e)})

@router.get('/document/{document_id}')
async def get_document_requirements(document_id:str):
    try:
        requirements = getDocumentRequirementsFromDB(document_id)
        # return {
        #     "message": "Document requirements are sent successfully",
        #     "requirements": requirements
        # }
        return requirements
    except Exception as e:
        raise HTTPException(status_code=400, detail="Document requirements cannot be fetched, Please try again later", headers={"X-Error": str(e)})

@router.get('/{requirement_id}')
async def get_requirement(requirement_id:str):
    try:
        requirement = getRequirementFromDB(requirement_id)
        # return {
        #     "message": "Requirement sent successfully",
        #     "requirement": requirement
        # }
        return requirement
    except Exception as e:
        raise HTTPException(status_code=400, detail="Requirements cannot be fetched, Please try again later", headers={"X-Error": str(e)})

## Edit requirement, validator to be added
@router.put("/{requirement_id}")
async def update_requirement(requirement_id: str, new_data: dict):
    try:
        updated = editRequirement(requirement_id, new_data)
        # return {
        #     "message": "Requirement updated successfully",
        #     "updated": updated
        # }
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail="Requirement cannot be accessed, Please try again later", headers={"X-Error": str(e)})

@router.delete("/{requirement_id}")
async def delete_requirement(requirement_id: str):
    try:
        if deleteRequirement(requirement_id) == True:
            # return {
            #     "message": "Requirement deleted successfully!"
            # }
            return True
    except Exception as e:
        raise HTTPException(status_code=400, detail="Requirement not found", headers={"X-Error": str(e)})