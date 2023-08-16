from fastapi import APIRouter, HTTPException, File, UploadFile
import os
from dotenv import load_dotenv

from mongodb import MongoDB
from bson.objectid import ObjectId
import pandas as pd

from src.models.models import SRSData
load_dotenv()

srs_database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

srs_main_collection = srs_database[os.environ.get("SRS_MAIN_COLLECTION")]
# srs_ids_collection = srs_database[os.environ.get("SRS_IDS_COLLECTION")]


#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/srs",
    responses={404: {"description": "Not found"}},
)

@router.get("/{srs_id}/")
async def get_srs_text(srs_id: str):
    try:
        object_id = ObjectId(srs_id)
        srs_document = srs_main_collection.find_one({"_id": object_id})
        
        if srs_document:

            response_body = {
                "message": "text found and sent successfully",
                "srs_id": srs_id,
                "srs_title": srs_document["srs_title"],
                "srs": srs_document["srs"]
            }
            
            return response_body
        else:
            raise HTTPException(status_code=400, detail="error in srs sending", headers={"X-Error": "SRS not found."})
    except Exception as e:
        raise HTTPException(status_code=400, detail="error in srs sending", headers={"X-Error": str(e)})

@router.post('/text/{project_id}/', status_code=201)
async def add_srs_text(project_id:str, srs_data: SRSData):
    text = srs_data.text
    srs_title = srs_data.srs_title
    # project_id = srs_data.project_id
    if not text:
        raise HTTPException(status_code=400, detail="error in text srs adding", headers={"X-Error": "Text cannot be empty."})

    # Insert the SRS data into the MongoDB collection.
    result = srs_main_collection.insert_one({
        "srs":text.split('\n'),
        "srs_title":srs_title,
        "project_id":project_id,
    })
    # if result:
    #     srs_id = str(result.inserted_id)
    #     srs_ids_collection.insert_one({
    #             "srs_id":srs_id,
    #             "srs_title":srs_title,
    #             "project_id":project_id,
    #         })
    response_body = {
        "message": "text srs added successfully",
        "srs_id": str(result.inserted_id)
    }

    return response_body

@router.post('/file/{project_id}/', status_code=201)
async def add_srs_file(project_id:str, file: UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file.file)
    result = srs_main_collection.insert_one({
        "srs":df.values.flatten().tolist(),
        "srs_title":file.filename,
        "project_id":project_id,
    })
    # if result:
    #     srs_id = str(result.inserted_id)
    #     srs_ids_collection.insert_one({
    #             "srs_id":srs_id,
    #             "srs_title":file.filename,
    #             "project_id":project_id,
    #         })
    response_body = {
        "message": "text srs added successfully",
        "srs_id": str(result.inserted_id)
    }

    return response_body
    #     print("print:"+df.__array__())
    # with open('uploads/'+file.filename, "wb") as f:
    #     f.write(await file.read())
    # return {
    #         'message': 'file srs added successfully',
    #         'srs_title':file.filename
    #         }

@router.put("/{srs_id}/")
async def update_project(srs_id: str, new_data: dict):
    try:
        # Convert the given document_id string to an ObjectId
        object_id = ObjectId(srs_id)

        # Use the update_one() method to update the document with the given object_id
        # The $set operator is used to update specific fields in the document
        result = srs_main_collection.update_one({"_id": object_id}, {"$set": new_data})

        # Check if the document was found and updated
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Srs not found")

        # result = srs_ids_collection.update_one({"srs_id": srs_id}, {"$set": new_data})

        # # Check if the document was found and updated
        # if result.matched_count == 0:
        #     raise HTTPException(status_code=404, detail="Srs not found")

        # Return a response indicating the update was successful
        return {"message": "Srs updated successfully"}

    except Exception as e:
        # Handle any potential exceptions and return an error response
        return {"error": str(e)}

@router.delete("/{srs_id}/")
async def delete_srs(srs_id: str):
    try:
        # Convert the given document_id string to an ObjectId
        object_id = ObjectId(srs_id)

        # Use the delete_one() method to delete the document with the given object_id
        result = srs_main_collection.delete_one({"_id": object_id})
        # result = srs_ids_collection.delete_one({"srs_id": srs_id})

        # Check if the document was found and deleted
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Document not found")

        # Return a response indicating the deletion was successful
        return {"message": "Document deleted successfully"}

    except Exception as e:
        # Handle any potential exceptions and return an error response
        return {"error": str(e)}