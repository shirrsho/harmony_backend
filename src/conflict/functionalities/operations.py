import os

from bson import ObjectId
from mongodb import MongoDB
from src.conflict.functionalities.algorithms import findConflicts
from src.report.functionalities.operations import addDocumentReport

database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]
conflict_collection = database[os.environ.get("CONFLICT_COLLECTION")]

def addConflictstoDB(requirements:any):
        #     "report_id": data.document_id,
        # "title":data.title,
        # "conflict_count":data.conflict_count,
        # "threat":data.threat,
        # "mark_as_safe":False
    
    conflicts = findConflicts(requirements)
    # for c in conflicts:
    #         conflict_collection.replace_one({"req1_id":c["req1_id"], "req2_id":c["req2_id"]}, c, upsert=True)
    added = conflict_collection.insert_many(conflicts)

    return added

def getDocumentConflicts(document_id:str):
    conflict_cursor = conflict_collection.find({"req1_document_id": document_id, "req2_document_id": document_id})
    conflicts = [{
        'id':str(conflict["_id"]),
        "req1_document_id": str(conflict["req1_document_id"]),
        "req2_document_id": str(conflict["req2_document_id"]),
        "project_id": str(conflict["project_id"]),
        "req1_id": str(conflict["req1_id"]),
        "req2_id": str(conflict["req2_id"]),
        "req2_content": str(conflict["req2_content"]),
        "req1_content": str(conflict["req1_content"]),
        'cos': str(conflict['cos']),
        'pos_overlap_ratio': str(conflict['pos_overlap_ratio']),
        'opposite_overlap_count': str(conflict['opposite_overlap_count']),
        'decision': str(conflict['decision']),
        'jaccard':str(conflict['jaccard']),
        'euclidean':str(conflict['euclidean']),
        'levenshtein':str(conflict['levenshtein']),
        'jensen_shannon':str(conflict['jensen_shannon']),
        'ngram':str(conflict['ngram']),
        'bm25':str(conflict['bm25']),
    } for conflict in conflict_cursor]
    return conflicts

def getProjectConflicts(project_id:str):
    conflict_cursor = conflict_collection.find({"project_id": project_id})
    conflicts = [{
        'id':str(conflict["_id"]),
        "req1_document_id": str(conflict["req1_document_id"]),
        "req2_document_id": str(conflict["req2_document_id"]),
        "project_id": str(conflict["project_id"]),
        "req1_id": str(conflict["req1_id"]),
        "req2_id": str(conflict["req2_id"]),
        "req2_content": str(conflict["req2_content"]),
        "req1_content": str(conflict["req1_content"]),
        'cos': str(conflict['cos']),
        'pos_overlap_ratio': str(conflict['pos_overlap_ratio']),
        'opposite_overlap_count': str(conflict['opposite_overlap_count']),
        'jaccard':str(conflict['jaccard']),
        'euclidean':str(conflict['euclidean']),
        'levenshtein':str(conflict['levenshtein']),
        'jensen_shannon':str(conflict['jensen_shannon']),
        'ngram':str(conflict['ngram']),
        'bm25':str(conflict['bm25']),
        'decision': str(conflict['decision'])
    } for conflict in conflict_cursor]
    return conflicts

def getConflict(conflict_id:str):
    conflict = conflict_collection.find_one({"_id":ObjectId(conflict_id)})
    return {
        'id':str(conflict["_id"]),
        "req1_document_id": str(conflict["req1_document_id"]),
        "req2_document_id": str(conflict["req2_document_id"]),
        "project_id": str(conflict["project_id"]),
        "req1_id": str(conflict["req1_id"]),
        "req2_id": str(conflict["req2_id"]),
        "req2_content": str(conflict["req2_content"]),
        "req1_content": str(conflict["req1_content"]),
        'cos': str(conflict['cos']),
        'pos_overlap_ratio': str(conflict['pos_overlap_ratio']),
        'opposite_overlap_count': str(conflict['opposite_overlap_count']),
        'jaccard':str(conflict['jaccard']),
        'euclidean':str(conflict['euclidean']),
        'levenshtein':str(conflict['levenshtein']),
        'jensen_shannon':str(conflict['jensen_shannon']),
        'ngram':str(conflict['ngram']),
        'bm25':str(conflict['bm25']),
        'decision': str(conflict['decision'])
    }

def editConflict(conflict_id:str, new_data:dict):
    conflict_collection.update_one({"_id": ObjectId(conflict_id)}, {"$set": new_data})

    return new_data

def deleteDocumentConflicts(document_id:str):
    return conflict_collection.delete_many({"req1_document_id": document_id, "req2_document_id": document_id})

def deleteProjectConflicts(project_id:str):
    return conflict_collection.delete_many({"project_id": project_id})