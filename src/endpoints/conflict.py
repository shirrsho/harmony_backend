# from fastapi import APIRouter, HTTPException
# import os
# from dotenv import load_dotenv
# from mongodb import MongoDB
# from bson import ObjectId
# from src.algorithms.cos import findstatus_intrasrs

# load_dotenv()

# srs_database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

# # srs_ids_collection = srs_database[os.environ.get("SRS_IDS_COLLECTION")]
# srs_projects_collection = srs_database[os.environ.get("SRS_PROJECTS_COLLECTION")]
# srs_main_collection = srs_database[os.environ.get("SRS_MAIN_COLLECTION")]
# srs_conflict_collection = srs_database[os.environ.get("SRS_CONFLICT_COLLECTION")]

# #APIRouter creates path operations for user module
# router = APIRouter(
#     prefix="/conflict",
#     responses={404: {"description": "Not found"}},
# )


# @router.post('/intra/{srs_id}/', status_code=201)
# async def find_intra_conflict(srs_id:str):
#     object_id = ObjectId(srs_id)
#     srs_document = srs_main_collection.find_one({"_id": object_id})

#     srsdf = srs_document["srs"]

#     conflictings = findstatus_intrasrs(srsdf)
#     safes = []

#     result = srs_conflict_collection.insert_one({
#         "srs_id":srs_id,
#         "conflict_set":conflictings,
#         "safe_set":safes
#     })
#     response_body = {
#             'message':'possible conflicts sent',
#             'conflict_set': conflictings
#         }
#     print(conflictings)
#     if result:
#         return response_body
#     else:
#         raise HTTPException(status_code=400, detail="error in conflict adding")


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
#         raise HTTPException(status_code=400, detail=e.__str__(), headers={"X-Error": str(e)})