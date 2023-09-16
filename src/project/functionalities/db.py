import os
from dotenv import load_dotenv
from mongodb import MongoDB
from bson import ObjectId

from src.document.functionalities.db import deleteProjectDocuments
from src.requirement.functionalities.db import deleteProjectRequirements

load_dotenv()

database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

project_collection = database[os.environ.get("PROJECT_COLLECTION")]
document_collection = database[os.environ.get("DOCUMENT_COLLECTION")]

def addProjecttoDB(data):
    result = project_collection.insert_one({
        "title":data.title
    })
    return result

def getProjectFromDB(project_id:str):
    project = project_collection.find_one({"_id": ObjectId(project_id)})

    return {
        "_id":str(project["_id"]),
        "title":str(project["title"])
    }

def getAllProjectsFromDB():
    projects_cursor = project_collection.find()
    projects = [{
        '_id':str(project["_id"]),
        'title':str(project["title"])
        } for project in projects_cursor]

    return projects

def editProject(project_id:str, new_data:dict):
    project_collection.update_one({"_id": ObjectId(project_id)}, {"$set": new_data})

    return new_data

def deleteProject(project_id:str):
    project_collection.delete_one({"_id": ObjectId(project_id)})
    try:
        deleteProjectDocuments(project_id)
        deleteProjectRequirements(project_id)
    except:
        pass

    return True