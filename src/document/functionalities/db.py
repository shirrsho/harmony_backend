import os
from dotenv import load_dotenv
from mongodb import MongoDB
from bson import ObjectId

from src.requirement.functionalities.db import deleteDocumentRequirements

load_dotenv()

database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

project_collection = database[os.environ.get("PROJECT_COLLECTION")]
document_collection = database[os.environ.get("DOCUMENT_COLLECTION")]


def addDocumenttoDB(data):
    result = document_collection.insert_one({
        "title":data.title,
        "project_id":data.project_id
    })
    return result

def getDocument(document_id:str):
    document = document_collection.find_one({"_id":ObjectId(document_id)})
    return {
        "_id":str(document["_id"]),
        "title":str(document["title"]),
        "project_id":str(document["project_id"])
    }

def getAllDocuments(project_id:str):
    # document_cursor = document_collection.find({"project_id": project_id},{'_id':1, 'title':1})
    document_cursor = document_collection.find({"project_id": project_id})
    documents = [{
        '_id':str(document["_id"]),
        'title':str(document["title"]),
        'project_id':project_id
    } for document in document_cursor]
    return documents


def editDocument(document_id:str, new_data:dict):
    document_collection.update_one({"_id": ObjectId(document_id)}, {"$set": new_data})

    return new_data

def deleteProjectDocuments(project_id:str):
    document_collection.delete_many({"project_id": project_id})
    return True

def deleteDocument(document_id:str):
    document_collection.delete_one({"_id": ObjectId(document_id)})
    try:
        deleteDocumentRequirements(document_id)
    except:
        pass

    return True