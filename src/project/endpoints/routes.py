from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from mongodb import MongoDB

from src.project.functionalities.db import addProjecttoDB, deleteProject, editProject, getAllProjectsFromDB, getProjectFromDB
from src.project.functionalities.validations import validateProject
from src.project.models.model import Project
load_dotenv()

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/project",
    responses={404: {"description": "Not found"}},
    tags=["Project"]
)

@router.post('/', status_code=201)
async def add_project(data: Project):
    validateProject(data)
    try:
        project = addProjecttoDB(data)
        return {
            "message": "Project added successfully!",
            "project_id": str(project.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Project cannot be added, Please try again later", headers={"X-Error": str(e)})

@router.get('/')
async def get_projects():
    try:
        projects = getAllProjectsFromDB()
        return {
            "message": "Projects are sent successfully",
            "projects": projects
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Projects cannot be fetched, Please try again later", headers={"X-Error": str(e)})

@router.get('/{project_id}')
async def get_project(project_id:str):
    try:
        project = getProjectFromDB(project_id)
        return {
            "message": "Project sent successfully",
            "project": project
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Projects cannot be fetched, Please try again later", headers={"X-Error": str(e)})

## Edit project, validator to be added
@router.put("/{project_id}/")
async def update_project(project_id: str, new_data: dict):
    try:
        updated = editProject(project_id, new_data)
        return {
            "message": "Project updated successfully",
            "updated": updated
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Project cannot be accessed, Please try again later", headers={"X-Error": str(e)})

@router.delete("/{project_id}/")
async def delete_project(project_id: str):
    try:
        if deleteProject(project_id) == True:
            return {
                "message": "Proejct deleted successfully!"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Project not found", headers={"X-Error": str(e)})