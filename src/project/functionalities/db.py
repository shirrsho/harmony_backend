import os
from dotenv import load_dotenv
from mongodb import MongoDB
from bson import ObjectId

load_dotenv()

database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

project_collection = database[os.environ.get("PROJECT_COLLECTION")]
document_collection = database[os.environ.get("DOCUMENT_COLLECTION")]

def addProjecttoDB(data):
    result = project_collection.insert_one({
        "title":data.title
    })
    return result

def getAllProjectsFromDB():
    projects_cursor = project_collection.find()
    projects = [{
        '_id':str(project["_id"]),
        'title':str(project["title"])
        } for project in projects_cursor]

    return projects

def editProject(project_id:str, new_data:dict):
    object_id = ObjectId(project_id)
    project_collection.update_one({"_id": object_id}, {"$set": new_data})

    return new_data

def deleteProjectDocuments(project_id:str):
    document_collection.delete_many({"project_id": project_id})

def deleteProject(project_id:str):
    object_id = ObjectId(project_id)
    project_collection.delete_one({"_id": object_id})
    try:
        deleteProjectDocuments(project_id)
    except:
        pass

    return True