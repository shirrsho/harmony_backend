from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv

from mongodb import MongoDB
from bson.objectid import ObjectId

from models import SRSData
load_dotenv()

database_name = os.environ.get("DATABASE_NAME")
srs_main_text_ep = os.environ.get("SRS_MAIN_TEXT_ENDPOINT")
srs_main_collection = os.environ.get("SRS_MAIN_COLLECTION")

app = FastAPI()

srs_database = MongoDB().get_client()[database_name]

@app.post(srs_main_text_ep, status_code=201)
async def add_srs_text(srs_data: SRSData):
    text = srs_data.text
    srs_title = srs_data.srs_title
    if not text:
        raise HTTPException(status_code=400, detail="error in text srs adding", headers={"X-Error": "Text cannot be empty."})

    # Insert the SRS data into the MongoDB collection.
    result = srs_database[srs_main_collection].insert_one({
        "srs":text,
        "srs_title":srs_title
    })
    srs_id = str(result.inserted_id)

    response_body = {
        "message": "text srs added successfully",
        "srs_id": srs_id
    }

    return response_body


# Get SRS

@app.get(srs_main_text_ep+"{srs_id}/")
async def get_srs_text(srs_id: str):
    try:
        object_id = ObjectId(srs_id)
        srs_document = srs_database[srs_main_collection].find_one({"_id": object_id})
        
        if srs_document:

            response_body = {
                "message": "text found and sent successfully",
                "srs_id": srs_id,
                "srs_title": srs_document["srs_title"],
                "srs": srs_document["srs"]
            }
            
            return response_body
        else:
            raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": "SRS not found."})
    except Exception as e:
        raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": str(e)})
