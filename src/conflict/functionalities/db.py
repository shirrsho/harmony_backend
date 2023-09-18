import os

from bson import ObjectId
from mongodb import MongoDB
from src.conflict.functionalities.algorithm import findConflicts

database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]
conflict_collection = database[os.environ.get("CONFLICT_COLLECTION")]

def addConflictstoDB(requirements:any):
    
    conflicts = findConflicts(requirements)
    
    added = conflict_collection.insert_many(conflicts)
    return added

def getDocumentConflicts(document_id:str):
    conflict_cursor = conflict_collection.find({"document_id": document_id})
    conflicts = [{
        'id':str(conflict["_id"]),
        "document_id": str(conflict["document_id"]),
        "project_id": str(conflict["project_id"]),
        "req1_id": str(conflict["req1_id"]),
        "req2_id": str(conflict["req2_id"]),
        'cos': str(conflict['cos']),
        'decision': str(conflict['decision'])
    } for conflict in conflict_cursor]
    return conflicts

def getProjectConflicts(project_id:str):
    conflict_cursor = conflict_collection.find({"project_id": project_id})
    conflicts = [{
        'id':str(conflict["_id"]),
        "document_id": str(conflict["document_id"]),
        "project_id": str(conflict["project_id"]),
        "req1_id": str(conflict["req1_id"]),
        "req2_id": str(conflict["req2_id"]),
        'cos': str(conflict['cos']),
        'decision': str(conflict['decision'])
    } for conflict in conflict_cursor]
    return conflicts

def getConflict(conflict_id:str):
    conflict = conflict_collection.find_one({"_id":ObjectId(conflict_id)})
    return {
        'id':str(conflict["_id"]),
        "document_id": str(conflict["document_id"]),
        "project_id": str(conflict["project_id"]),
        "req1_id": str(conflict["req1_id"]),
        "req2_id": str(conflict["req2_id"]),
        'cos': str(conflict['cos']),
        'decision': str(conflict['decision'])
    }
