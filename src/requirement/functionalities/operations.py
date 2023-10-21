import os
from dotenv import load_dotenv
from mongodb import MongoDB
from bson import ObjectId

from src.requirement.functionalities.algorithms import extractPosTokens

load_dotenv()

database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

project_collection = database[os.environ.get("PROJECT_COLLECTION")]
document_collection = database[os.environ.get("DOCUMENT_COLLECTION")]
requirement_collection = database[os.environ.get("REQUIREMENT_COLLECTION")]

def addRequirementtoDB(data):
    word_objects = extractPosTokens(data.content)
    result = requirement_collection.insert_one({
        "document_id": data.document_id,
        "project_id": data.project_id,
        "content": data.content,
        "word_objects": word_objects
    })
    return result

def addDocumentRequirementstoDB(data):
    # result = requirement_collection.insert_one({
    #     "document_id": data.document_id,
    #     "project_id": data.project_id,
    #     "content": data.content
    # })
    for d in data:
        d["word_objects"] = extractPosTokens(str(d["content"]))
        print(d)
    result = requirement_collection.insert_many(data)
    
    return result

def getProjectRequirementsFromDB(project_id:str):
    requirements_cursor = requirement_collection.find({"project_id":project_id})
    requirements = [{
        "document_id": str(req["document_id"]),
        "project_id": str(req["project_id"]),
        "content": str(req["content"]),
        "word_objects": str(req["word_objects"]),
        'id':str(req["_id"])
        } for req in requirements_cursor]

    return requirements

def getDocumentRequirementsFromDB(document_id:str):
    requirements_cursor = requirement_collection.find({"document_id":document_id})
    requirements = [{
        "document_id": str(req["document_id"]),
        "project_id": str(req["project_id"]),
        "content": str(req["content"]),
        "word_objects": str(req["word_objects"]),
        'id':str(req["_id"])
        } for req in requirements_cursor]

    return requirements

def getRequirementFromDB(requirement_id:str):
    req = requirement_collection.find_one({"_id": ObjectId(requirement_id)})

    return {
        "document_id": str(req["document_id"]),
        "project_id": str(req["project_id"]),
        "content": str(req["content"]),
        "word_objects": str(req["word_objects"]),
        'id':str(req["_id"])
    }

def editRequirement(requirement_id:str, new_data:dict):
    requirement_collection.update_one({"_id": ObjectId(requirement_id)}, {"$set": new_data})
    return new_data

def deleteProjectRequirements(project_id:str):
    requirement_collection.delete_many({"project_id": project_id})
    return True

def deleteDocumentRequirements(document_id:str):
    requirement_collection.delete_many({"document_id": document_id})
    return True

def deleteRequirement(requirement_id:str):
    requirement_collection.delete_one({"_id": ObjectId(requirement_id)})
    return True