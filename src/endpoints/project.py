# from fastapi import APIRouter, HTTPException
# import os
# from dotenv import load_dotenv
# from mongodb import MongoDB
# from bson import ObjectId
# from src.models.models import SRSProject
# load_dotenv()

# srs_database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

# # srs_ids_collection = srs_database[os.environ.get("SRS_IDS_COLLECTION")]
# srs_projects_collection = srs_database[os.environ.get("SRS_PROJECTS_COLLECTION")]
# srs_main_collection = srs_database[os.environ.get("SRS_MAIN_COLLECTION")]

# #APIRouter creates path operations for user module
# router = APIRouter(
#     prefix="/project",
#     responses={404: {"description": "Not found"}},
# )

# @router.post('/', status_code=201)
# async def add_project(data: SRSProject):
#     project_title = data.project_title
#     if not project_title:
#         raise HTTPException(status_code=400, detail="error in text srs adding", headers={"X-Error": "Text cannot be empty."})

#     # Insert the SRS data into the MongoDB collection.
#     result = srs_projects_collection.insert_one({
#         "project_title":project_title
#     })

#     response_body = {
#         "message": "project added successfully",
#         "project_id": str(result.inserted_id)
#     }

#     return response_body

# @router.get('/')
# async def get_projects():
#     try:
#         srs_projects_cursor = srs_projects_collection.find()
#         srs_projects = [{
#             'project_id':str(srs_project["_id"]),
#             'project_title':str(srs_project["project_title"])
#             } for srs_project in srs_projects_cursor]

#         response_body = {
#             "message": "projects found and sent successfully",
#             "srs_projects": srs_projects
#         }
            
#         return response_body
        
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": str(e)})
        
# @router.get("/{project_id}/")
# async def get_project(project_id: str):
#     try:
#         # object_id = ObjectId(srs_id)
#         # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        
#         srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
#         srs_ids = [{
#             'srs_id':str(srs_ids["_id"]),
#             'srs_title':str(srs_ids["srs_title"])
#         } for srs_ids in srs_ids_cursor]

#         if srs_ids:
#             response_body = {
#                 "message": "project found and srss sent successfully",
#                 "srs_ids": srs_ids
#             }

#             return response_body
#         else:
#             raise HTTPException(status_code=400, detail="not found", headers={"X-Error": "project not found."})
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="error in project srss sending", headers={"X-Error": str(e)})

# @router.put("/{project_id}/")
# async def update_project(project_id: str, new_data: dict):
#     try:
#         # Convert the given document_id string to an ObjectId
#         object_id = ObjectId(project_id)

#         # Use the update_one() method to update the document with the given object_id
#         # The $set operator is used to update specific fields in the document
#         result = srs_projects_collection.update_one({"_id": object_id}, {"$set": new_data})

#         # Check if the document was found and updated
#         if result.matched_count == 0:
#             raise HTTPException(status_code=404, detail="Project not found")

#         # Return a response indicating the update was successful
#         return {"message": "Project updated successfully"}

#     except Exception as e:
#         # Handle any potential exceptions and return an error response
#         return {"error": str(e)}

# @router.delete("/{project_id}/")
# async def delete_project(project_id: str):
#     try:
#         # Convert the given document_id string to an ObjectId
#         object_id = ObjectId(project_id)

#         # Use the delete_one() method to delete the document with the given object_id
#         result = srs_projects_collection.delete_one({"_id": object_id})
#         # result = srs_ids_collection.delete_many({"project_id": project_id})
#         result = srs_main_collection.delete_many({"project_id": project_id})

#         # Check if the document was found and deleted
#         if result.deleted_count == 0:
#             raise HTTPException(status_code=404, detail="Document not found")

#         # Return a response indicating the deletion was successful
#         return {"message": "Document deleted successfully"}

#     except Exception as e:
#         # Handle any potential exceptions and return an error response
#         return {"error": str(e)}