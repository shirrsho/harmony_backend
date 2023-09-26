from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from mongodb import MongoDB
from bson import ObjectId
from src.conflict.functionalities.db import addConflictstoDB, deleteDocumentConflicts, deleteProjectConflicts, getConflict, getDocumentConflicts, getProjectConflicts
from src.conflict.models.model import Conflict
from src.document.functionalities.db import getDocument
from src.project.functionalities.db import getProjectFromDB
from src.report.functionalities.db import addDocumentReport, addProjectReport, getDocumentReport, getProjectReport
from src.requirement.functionalities.db import getDocumentRequirementsFromDB, getProjectRequirementsFromDB

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


@router.post('/document', status_code=201)
async def find_document_conflict(document_id:str):
    
    # return requirements
    # added_conflicts = addConflictstoDB(requirements)
    # {isConflicting, cos} 

    try:
        report = getDocumentReport(document_id) # External call
        if report != None: return []
        requirements = getDocumentRequirementsFromDB(document_id) # External call
        result = addConflictstoDB(requirements)
        
        document = getDocument(document_id)
        addDocumentReport({
            "document_id": document_id,
            "title":document["title"],
            "conflict_count":result.inserted_ids.__len__(),
            "threat":0.0
        }) # External call
        
        return {
            "message": "Conflicts successfully found!",
            "conflict_ids": [str(id) for id in result.inserted_ids]
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Conflicts can not be found!", headers={"X-Error": str(e)})
    
@router.post('/project', status_code=201)
async def find_project_conflict(project_id:str):
    
    # return requirements
    # added_conflicts = addConflictstoDB(requirements)
    # {isConflicting, cos}

    try:
        report = getProjectReport(project_id) # External call
        if report != None: return []
        requirements = getProjectRequirementsFromDB(project_id) # External call
        
        result = addConflictstoDB(requirements)
        project = getProjectFromDB(project_id) # External call
        addProjectReport({
            "project_id": project_id,
            "title":project["title"],
            "conflict_count":result.inserted_ids.__len__(),
            "threat":0.0
        }) # External call

        # return {
        #     "message": "Conflicts successfully found!",
        #     "conflict_ids": [str(id) for id in result.inserted_ids]
        # }
        return [str(id) for id in result.inserted_ids]
    except Exception as e:
        raise HTTPException(status_code=404, detail="Conflicts can not be found!", headers={"X-Error": str(e)})
    
@router.get("/document/{document_id}")
async def get_document_conflicts(document_id: str):
    try:
        # object_id = ObjectId(srs_id)
        # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        conflicts = getDocumentConflicts(document_id)

        # return {
        #         "message": "Document conflict found!",
        #         "conflicts": conflicts
        # }
        return conflicts
    except Exception as e:
        raise HTTPException(status_code=400, detail="Document conflict cannot be accessed, Please try again later", headers={"X-Error": str(e)})
    
@router.get("/project/{project_id}")
async def get_project_conflicts(project_id: str):
    try:
        # object_id = ObjectId(srs_id)
        # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        conflicts = getProjectConflicts(project_id)


        # return {
        #         "message": "Project conflict found!",
        #         "conflicts": conflicts
        # }
        return conflicts
    except Exception as e:
        raise HTTPException(status_code=400, detail="Project conflict cannot be accessed, Please try again later", headers={"X-Error": str(e)})

@router.delete("/document/{document_id}")
async def delete_document_conflicts(document_id: str):
    try:
        deleteDocumentConflicts(document_id)
        # object_id = ObjectId(srs_id)
        # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        # conflicts = getDocumentConflicts(document_id)

        # return {
        #         "message": "Document conflict found!",
        #         "conflicts": conflicts
        # }
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail="Conflicts cannot be accessed, Please try again later", headers={"X-Error": str(e)})
    
@router.delete("/project/{project_id}")
async def delete_project_conflicts(project_id: str):
    try:
        # object_id = ObjectId(srs_id)
        # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        # conflicts = getProjectConflicts(project_id)


        # return {
        #         "message": "Project conflict found!",
        #         "conflicts": conflicts
        # }
        deleteProjectConflicts(project_id)
        # object_id = ObjectId(srs_id)
        # srs_ids_cursor = srs_main_collection.find({"project_id": project_id},{'_id':1, 'srs_title':1})
        # conflicts = getDocumentConflicts(document_id)

        # return {
        #         "message": "Document conflict found!",
        #         "conflicts": conflicts
        # }
        return True
        # return conflicts
    except Exception as e:
        raise HTTPException(status_code=400, detail="Conflicts cannot be accessed, Please try again later", headers={"X-Error": str(e)})
    
@router.get("/{conflict_id}")
async def get_conflict(conflict_id: str):
    try:
        conflict = getConflict(conflict_id)
        
        # return {
        #         "message": "Conflict found and sent successfully",
        #         "conflict": conflict
        #     }
        return conflict
    except Exception as e:
        raise HTTPException(status_code=400, detail="Conflict not found!", headers={"X-Error": str(e)})