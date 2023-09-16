from fastapi import APIRouter, HTTPException, File, UploadFile
import os
from dotenv import load_dotenv

from mongodb import MongoDB
from bson.objectid import ObjectId
import pandas as pd
from src.document.functionalities.validations import validateDocument

from src.document.models.model import SRSData
load_dotenv()

# srs_database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

# srs_main_collection = srs_database[os.environ.get("SRS_MAIN_COLLECTION")]
# # srs_ids_collection = srs_database[os.environ.get("SRS_IDS_COLLECTION")]


#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/document",
    responses={404: {"description": "Not found"}},
    tags=["Document"]
)

# @router.get("/all/{project_id}/")
# async def get_documents(project_id: str):
#     try:
#         # object_id = ObjectId(srs_id)
#         # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        
#         srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
#         srs_ids = [{
#             'srs_id':str(srs_ids["_id"]),
#             'srs_title':str(srs_ids["srs_title"])
#         } for srs_ids in srs_ids_cursor]

#         return {
#                 "message": "Project found and documents sent successfully",
#                 "srs_ids": srs_ids
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Project cannot be accessed, Please try again later", headers={"X-Error": str(e)})

# @router.get("/{srs_id}/")
# async def get_srs_text(srs_id: str):
#     try:
#         object_id = ObjectId(srs_id)
#         srs_document = srs_main_collection.find_one({"_id": object_id})
        
#         return {
#                 "message": "text found and sent successfully",
#                 "srs_id": srs_id,
#                 "srs_title": srs_document["srs_title"],
#                 "srs": srs_document["srs"]
#             }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Document not found!", headers={"X-Error": str(e)})

# @router.post('/text/{project_id}/', status_code=201)
# async def add_srs_text(project_id:str, srs_data: SRSData):
#     validateDocument(srs_data)
#     text = srs_data.text
#     srs_title = srs_data.srs_title
#     # project_id = srs_data.project_id

#     # Insert the SRS data into the MongoDB collection.
#     try:
#         result = srs_main_collection.insert_one({
#             "srs":text.split('\n'),
#             "srs_title":srs_title,
#             "project_id":project_id,
#         })

#         return {
#             "message": "text srs added successfully",
#             "srs_id": str(result.inserted_id)
#         }
#     except:
#         raise HTTPException(status_code=404, detail="Document can not be added!")

# @router.post('/file/{project_id}/', status_code=201)
# async def add_srs_file(project_id:str, file: UploadFile = File(...)):
#     if file.filename.endswith('.csv'):
#         df = pd.read_csv(file.file)
#     try:
#         result = srs_main_collection.insert_one({
#             "srs":df.values.flatten().tolist(),
#             "srs_title":file.filename,
#             "project_id":project_id,
#         })

#         return {
#             "message": "text srs added successfully",
#             "srs_id": str(result.inserted_id)
#         }
#     except:
#         raise HTTPException(status_code=404, detail="File can not be added!")

# #Validators to be added
# @router.put("/{srs_id}/")
# async def update_project(srs_id: str, new_data: dict):
#     try:
#         object_id = ObjectId(srs_id)

#         srs_main_collection.update_one({"_id": object_id}, {"$set": new_data})

#         return {
#             "message": "Document updated successfully",
#             "updated": new_data
#         }

#     except Exception as e:
#         # Handle any potential exceptions and return an error response
#         raise HTTPException(status_code=404, detail="Document can not be updated", headers={"X-Error": str(e)})

# @router.delete("/{srs_id}/")
# async def delete_srs(srs_id: str):
#     try:
#         # Convert the given document_id string to an ObjectId
#         object_id = ObjectId(srs_id)

#         srs_main_collection.delete_one({"_id": object_id})
#         # result = srs_ids_collection.delete_one({"srs_id": srs_id})

#         # Return a response indicating the deletion was successful
#         return {"message": "Document deleted successfully"}

#     except Exception as e:
#         # Handle any potential exceptions and return an error response
#         raise HTTPException(status_code=404, detail="Document can not be deleted", headers={"X-Error": str(e)})