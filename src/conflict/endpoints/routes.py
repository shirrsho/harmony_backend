from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from mongodb import MongoDB
from bson import ObjectId
from src.conflict.functionalities.cos import findstatus_intrasrs

load_dotenv()

# srs_database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

# # srs_ids_collection = srs_database[os.environ.get("SRS_IDS_COLLECTION")]
# srs_projects_collection = srs_database[os.environ.get("SRS_PROJECTS_COLLECTION")]
# srs_main_collection = srs_database[os.environ.get("SRS_MAIN_COLLECTION")]
# srs_conflict_collection = srs_database[os.environ.get("SRS_CONFLICT_COLLECTION")]

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/conflict",
    responses={404: {"description": "Not found"}},
    tags=["Conflict"]
)


# @router.post('/intra/{srs_id}/', status_code=201)
# async def find_intra_conflict(srs_id:str):
#     object_id = ObjectId(srs_id)
#     try:
#         srs_document = srs_main_collection.find_one({"_id": object_id})
#     except:
#         raise HTTPException(status_code=400, detail="No data available!")

#     srsdf = srs_document["srs"]

#     conflictings = findstatus_intrasrs(srsdf)
#     safes = []

#     try:
#         srs_conflict_collection.insert_one({
#             "srs_id":srs_id,
#             "conflict_set":conflictings,
#             "safe_set":safes
#         })
#         return {
#                 'message':'possible conflicts sent',
#                 'conflict_set': conflictings
#             }
#     except:
#         raise HTTPException(status_code=400, detail="Cannot find conflicts!")


# @router.get('/intra/{srs_id}/', status_code=200)
# async def get_intra_conflicts(srs_id:str):
#     try:
#         srs_conflicts = srs_conflict_collection.find_one({"srs_id": srs_id})
        
#         if srs_conflicts:
#             response_body = {
#                 "message": "conflicts found and sent successfully",
#                 "srs_conflicts": srs_conflicts["conflict_set"],
#                 "srs_safes": srs_conflicts["safe_set"]
#             }
#         else:
#             response_body = {
#                 "message": "conflicts not found",
#                 "srs_conflicts": [],
#                 "srs_safes": []
#             }
#         return response_body
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Cannot get!", headers={"X-Error": str(e)})