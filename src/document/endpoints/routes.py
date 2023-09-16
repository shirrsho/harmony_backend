from fastapi import APIRouter, HTTPException, File, UploadFile
import os
from dotenv import load_dotenv

from mongodb import MongoDB
from bson.objectid import ObjectId
import pandas as pd
from src.document.functionalities.db import addDocumenttoDB, deleteDocument, editDocument, getAllDocuments, getDocument
from src.document.functionalities.validations import validateDocument

from src.document.models.model import Document
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

@router.get("/all/{project_id}/")
async def get_documents(project_id: str):
    try:
        # object_id = ObjectId(srs_id)
        # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        documents = getAllDocuments(project_id)


        return {
                "message": "Project found and documents sent successfully",
                "documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Project cannot be accessed, Please try again later", headers={"X-Error": str(e)})

@router.get("/{document_id}/")
async def get_document(document_id: str):
    try:
        document = getDocument(document_id)
        
        return {
                "message": "text found and sent successfully",
                "document": document
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Document not found!", headers={"X-Error": str(e)})

@router.post('/', status_code=201)
async def add_document(data: Document):
    validateDocument(data)
    try:
        result = addDocumenttoDB(data)
        return {
            "message": "text srs added successfully",
            "document_id": str(result.inserted_id)
        }
    except:
        raise HTTPException(status_code=404, detail="Document can not be added!")

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

#Validators to be added
@router.put("/{document_id}/")
async def update_document(document_id: str, new_data: dict):
    try:
        updated = editDocument(document_id, new_data)

        return {
            "message": "Document updated successfully",
            "updated": updated
        }

    except Exception as e:
        # Handle any potential exceptions and return an error response
        raise HTTPException(status_code=404, detail="Document can not be updated", headers={"X-Error": str(e)})

@router.delete("/{document_id}/")
async def delete_document(document_id: str):
    try:
        if deleteDocument(document_id) == True:
            return {
                "message": "Document deleted successfully!"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Document not found", headers={"X-Error": str(e)})