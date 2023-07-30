from fastapi import APIRouter, HTTPException, File, UploadFile
import os
from dotenv import load_dotenv

from mongodb import MongoDB
from bson.objectid import ObjectId

from src.models.models import SRSData
load_dotenv()

database_name = os.environ.get("DATABASE_NAME")
srs_main_collection = os.environ.get("SRS_MAIN_COLLECTION")
srs_ids_collection = os.environ.get("SRS_IDS_COLLECTION")
srs_projects_collection = os.environ.get("SRS_PROJECTS_COLLECTION")

srs_database = MongoDB().get_client()[database_name]

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/srs",
    responses={404: {"description": "Not found"}},
)

@router.get('/'+"{project_id}/")
async def get_srs_ids(project_id:str):
    try:
        srs_ids_cursor = srs_database[srs_ids_collection].find_all({"project_id": project_id})
        srs_ids = [{
            'srs_id':str(srs_ids["_id"]),
            'srs_title':str(srs_ids["srs_title"])
            } for srs_ids in srs_ids_cursor]

        response_body = {
            "message": "ids found and sent successfully",
            "srs_ids": srs_ids
        }
        
        return response_body
    except Exception as e:
        raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": str(e)})

@router.get('/'+"{srs_id}/")
async def get_srs_text(srs_id: str):
    try:
        object_id = ObjectId(srs_id)
        srs_document = srs_database[srs_main_collection].find_one({"_id": object_id})
        
        if srs_document:

            response_body = {
                "message": "text found and sent successfully",
                "srs_id": srs_id,
                "srs_title": srs_document["srs_title"],
                "srs": srs_document["srs"]
            }
            
            return response_body
        else:
            raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": "SRS not found."})
    except Exception as e:
        raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": str(e)})

@router.post('/text/', status_code=201)
async def add_srs_text(srs_data: SRSData):
    text = srs_data.text
    srs_title = srs_data.srs_title
    project_id = srs_data.project_id
    if not text:
        raise HTTPException(status_code=400, detail="error in text srs adding", headers={"X-Error": "Text cannot be empty."})

    # Insert the SRS data into the MongoDB collection.
    result = await srs_database[srs_main_collection].insert_one({
        "srs":text,
        "srs_title":srs_title,
        "project_id":project_id,
    })
    if result:
        srs_id = str(result.inserted_id)
        await srs_database[srs_ids_collection].insert_one({
                "srs_id":srs_id,
                "srs_title":srs_title,
                "project_id":project_id,
            })
    response_body = {
        "message": "text srs added successfully",
        "srs_id": srs_id
    }

    return response_body

@router.post('/file/', status_code=201)
async def add_srs_file(file: UploadFile = File(...)):
    # ufile = file
    # srs_title = srs_data.srs_title
    # Handle the uploaded file here
    # You can save the file, process it, etc.
    # For example, to save it to a specific location:
    with open('uploads/'+file.filename, "wb") as f:
        f.write(await file.read())
    return {
            'message': 'file srs added successfully',
            'srs_title':file.filename
            }