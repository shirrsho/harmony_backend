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

@router.post('/intra/{srs_id}/', status_code=201)
async def find_intra_conflict(srs_id:str):
    object_id = ObjectId(srs_id)
    srs_document = srs_main_collection.find_one({"_id": object_id})
    df = srs_document["srs"]
    tfidf_matrix = tfidf.fit_transform(df)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    conflictings = set([])
    for i in range(len(df)):
        for j in range(len(df)):
            if(cosine_sim[i-1][j-1]>0.5):
                if(i!=j):
                    conflictings.add(i)
                    conflictings.add(j)
    conflictings = list(conflictings)
    result = srs_conflict_collection.insert_one({
        "srs_id":srs_id,
        "conflict_set":conflictings
    })
    response_body = {
            'message':'possible conflicts sent',
            'conflict_set': conflictings
        }
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
                "srs_conflicts": srs_conflicts["conflict_set"]
            }
        else:
            response_body = {
                "message": "conflicts not found",
                "srs_conflicts": []
            }
        return response_body
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.__str__(), headers={"X-Error": str(e)})