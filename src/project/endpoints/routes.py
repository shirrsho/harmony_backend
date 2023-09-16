from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from mongodb import MongoDB
from bson import ObjectId
from src.project.functionalities.validations import validateProject
from src.project.models.model import SRSProject
load_dotenv()

srs_database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

# srs_ids_collection = srs_database[os.environ.get("SRS_IDS_COLLECTION")]
srs_projects_collection = srs_database[os.environ.get("SRS_PROJECTS_COLLECTION")]
srs_main_collection = srs_database[os.environ.get("SRS_MAIN_COLLECTION")]

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/project",
    responses={404: {"description": "Not found"}},
    tags=["Project"]
)

@router.post('/', status_code=201)
async def add_project(data: SRSProject):
    validateProject(data)
    project_title = data.project_title

    # Insert the SRS data into the MongoDB collection.
    try:
        result = srs_projects_collection.insert_one({
            "project_title":project_title
        })
        return {
            "message": "Project added successfully",
            "project_id": str(result.inserted_id)
        }
    except:
        return {
            "message": "Please try again later"
        }


@router.get('/')
async def get_projects():
    try:
        srs_projects_cursor = srs_projects_collection.find()
        srs_projects = [{
            'project_id':str(srs_project["_id"]),
            'project_title':str(srs_project["project_title"])
            } for srs_project in srs_projects_cursor]

        return {
            "message": "Projects are sent successfully",
            "srs_projects": srs_projects
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Projects cannot be added, Please try again later", headers={"X-Error": str(e)})
        
@router.get("/{project_id}/")
async def get_documents(project_id: str):
    try:
        # object_id = ObjectId(srs_id)
        # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        
        srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        srs_ids = [{
            'srs_id':str(srs_ids["_id"]),
            'srs_title':str(srs_ids["srs_title"])
        } for srs_ids in srs_ids_cursor]

        return {
                "message": "Project found and documents sent successfully",
                "srs_ids": srs_ids
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Project cannot be accessed, Please try again later", headers={"X-Error": str(e)})

## Edit project, validator to be added
@router.put("/{project_id}/")
async def update_project(project_id: str, new_data: dict):
    try:
        object_id = ObjectId(project_id)
        result = srs_projects_collection.update_one({"_id": object_id}, {"$set": new_data})

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")

        return {
            "message": "Project updated successfully",
            "updated": new_data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail="Project cannot be accessed, Please try again later", headers={"X-Error": str(e)})

@router.delete("/{project_id}/")
async def delete_project(project_id: str):
    try:
        object_id = ObjectId(project_id)
        srs_projects_collection.delete_one({"_id": object_id})
        try:
            srs_main_collection.delete_many({"project_id": project_id})
        except:
            pass

        return {
            "message": "Proejct deleted successfully!"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail="Project not found", headers={"X-Error": str(e)})