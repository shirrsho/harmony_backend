import os

from bson import ObjectId
from mongodb import MongoDB
from src.conflict.functionalities.algorithms import findConflicts

database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]
report_collection = database[os.environ.get("REPORT_COLLECTION")]



def addDocumentReport(data:any):
    
    report_collection.insert_one({
        "report_id": data["document_id"],
        "title":data["title"],
        "conflict_count":data["conflict_count"],
        "threat":data["threat"],
        "mark_as_safe":False
    })
    return True

def editProjectReport(project_id:str, new_data:dict):
    report_collection.update_one({"report_id": project_id}, {"$set": new_data})
    return new_data

def addProjectReport(data:dict):
    report_collection.insert_one({
        "report_id": data["project_id"],
        "title":data["title"],
        "conflict_count":data["conflict_count"],
        "threat":data["threat"],
        "mark_as_safe":False
    })
    return True

def editDocumentReport(document_id:str, new_data:dict):
    report_collection.update_one({"report_id": document_id}, {"$set": new_data})
    return new_data

def addRequirementReport(data:dict):
    report_collection.insert_one({
        "report_id": data.requirment_id,
        "content":data.content,
        "conflicted":data.conflicted,
        "mark_as_safe":False
    })
    return True

def editRequirementReport(requirement_id:str, new_data:dict):
    report_collection.update_one({"report_id": requirement_id}, {"$set": new_data})
    return new_data

def getDocumentReport(document_id:str):
    report = report_collection.find_one({"report_id": document_id})
    return report

def getProjectReport(project_id:str):
    report = report_collection.find_one({"report_id": project_id})
    return report

def getRequirementReport(requirement_id:str):
    report = report_collection.find_one({"report_id": requirement_id})
    return report
