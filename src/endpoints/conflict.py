from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from mongodb import MongoDB
from bson import ObjectId
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()

tfidf = TfidfVectorizer()

srs_database = MongoDB().get_client()[os.environ.get("DATABASE_NAME")]

srs_ids_collection = srs_database[os.environ.get("SRS_IDS_COLLECTION")]
srs_projects_collection = srs_database[os.environ.get("SRS_PROJECTS_COLLECTION")]
srs_main_collection = srs_database[os.environ.get("SRS_MAIN_COLLECTION")]
srs_conflict_collection = srs_database[os.environ.get("SRS_CONFLICT_COLLECTION")]

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/conflict",
    responses={404: {"description": "Not found"}},
)

def insertin(conflictings, toinsert):
    # Check if any of the numbers in the new_set exist in any of the sets in the array
    combined_sets = []
    for existing_set in conflictings:
        if any(num in existing_set for num in toinsert):
            combined_sets.append(existing_set)
    
    # If there are two or more sets to combine, create a union of them
    if len(combined_sets) >= 1:
        combined_union = set(toinsert)
        for existing_set in combined_sets:
            combined_union |= existing_set
        
        # Remove the combined sets from the array
        conflictings = [s for s in conflictings if s not in combined_sets]
        
        # Append the combined union set to the array
        conflictings.append(combined_union)
    else:
        conflictings.append(set(toinsert))

    # ret = []
    
    # for set1 in conflictings:
    #     for set2 in conflictings:
    #         if set1.intersection(set2)!={}:
    #             ret.append(set1.union(set2))
    print("Hi",toinsert,conflictings)
    return conflictings

def findstatus_intrasrs(srs_count, cosine_sim_matrix):
    conflictings = []

    for i in range(srs_count):
        for j in range(srs_count):
            if(cosine_sim_matrix[i][j]>0.5):
                if(i!=j):
                    conflictings = insertin(conflictings, set((i,j)))
    # print(cosine_sim_matrix)
    # print(conflictings)

    ret = [[]]
    
    for c in conflictings:
        c = list(c)
        ret.append(c)
    return ret


@router.post('/intra/{srs_id}/', status_code=201)
async def find_intra_conflict(srs_id:str):
    object_id = ObjectId(srs_id)
    srs_document = srs_main_collection.find_one({"_id": object_id})

    srsdf = srs_document["srs"]
    tfidf_matrix = tfidf.fit_transform(srsdf)
    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    conflictings = findstatus_intrasrs(len(srsdf), cosine_sim_matrix)

    # print(cosine_sim_matrix)
    # print(conflictings)

    # conflictings = set([])
    safes = []
    # for i in range(len(df)):
    #     for j in range(len(df)):
    #         if(cosine_sim[i-1][j-1]>0.5):
    #             if(i!=j):
    #                 conflictings.add(i)
    #                 conflictings.add(j)
    # for i in range(len(df)):
    #     if i not in conflictings:
    #         safes.add(i)
    # conflictings = list(conflictings)
    # safes = list(safes)
    result = srs_conflict_collection.insert_one({
        "srs_id":srs_id,
        "conflict_set":conflictings,
        "safe_set":safes
    })
    response_body = {
            'message':'possible conflicts sent',
            'conflict_set': conflictings
        }
    print(conflictings)
    if result:
        return response_body
    else:
        raise HTTPException(status_code=400, detail="error in conflict adding")


@router.get('/intra/{srs_id}/', status_code=200)
async def get_intra_conflicts(srs_id:str):
    try:
        srs_conflicts = srs_conflict_collection.find_one({"srs_id": srs_id})
        
        if srs_conflicts:
            response_body = {
                "message": "conflicts found and sent successfully",
                "srs_conflicts": srs_conflicts["conflict_set"],
                "srs_safes": srs_conflicts["safe_set"]
            }
        else:
            response_body = {
                "message": "conflicts not found",
                "srs_conflicts": [],
                "srs_safes": []
            }
        return response_body
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.__str__(), headers={"X-Error": str(e)})