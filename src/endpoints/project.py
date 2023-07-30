from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from mongodb import MongoDB
from src.models.models import SRSProject
load_dotenv()

database_name = os.environ.get("DATABASE_NAME")
srs_main_collection = os.environ.get("SRS_MAIN_COLLECTION")
srs_ids_collection = os.environ.get("SRS_IDS_COLLECTION")
srs_projects_collection = os.environ.get("SRS_PROJECTS_COLLECTION")

srs_database = MongoDB().get_client()[database_name]

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/project",
    responses={404: {"description": "Not found"}},
)

@router.post('/', status_code=201)
async def add_project(data: SRSProject):
    project_title = data.project_title
    if not project_title:
        raise HTTPException(status_code=400, detail="error in text srs adding", headers={"X-Error": "Text cannot be empty."})

    # Insert the SRS data into the MongoDB collection.
    result = srs_database[srs_projects_collection].insert_one({
        "project_title":project_title
    })

    response_body = {
        "message": "project added successfully",
        "srs_id": str(result.inserted_id)
    }

    return response_body

@router.get('/')
async def get_projects():
    try:
        srs_projects_cursor = srs_database[srs_projects_collection].find()
        srs_projects = [{
            'project_id':str(srs_project["_id"]),
            'project_title':str(srs_project["project_title"])
            } for srs_project in srs_projects_cursor]

        response_body = {
            "message": "projects found and sent successfully",
            "srs_projects": srs_projects
        }
            
        return response_body
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": str(e)})
        
@router.get('/'+"{project_id}/")
async def get_srs_text(project_id: str):
    try:
        # object_id = ObjectId(srs_id)
        srs_ids_cursor = srs_database[srs_ids_collection].find_all({"project_id": project_id})
        srs_ids = [{
            'srs_id':str(srs_ids["srs_id"]),
            'srs_title':str(srs_ids["srs_title"])
            } for srs_ids in srs_ids_cursor]

        if srs_ids:
            response_body = {
                "message": "project found and srss sent successfully",
                "srs_ids": srs_ids
            }

            return response_body
        else:
            raise HTTPException(status_code=400, detail="error in project srss sending", headers={"X-Error": "project not found."})
    except Exception as e:
        raise HTTPException(status_code=400, detail="error in project srss sending", headers={"X-Error": str(e)})