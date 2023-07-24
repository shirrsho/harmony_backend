from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from mongodb import MongoDB
from bson.objectid import ObjectId

from models import SRSData, SRSFile
load_dotenv()

database_name = os.environ.get("DATABASE_NAME")
srs_main_collection = os.environ.get("SRS_MAIN_COLLECTION")
srs_ids_collection = os.environ.get("SRS_IDS_COLLECTION")

srs_main_text_ep = os.environ.get("SRS_MAIN_TEXT_ENDPOINT")
srs_main_file_ep = os.environ.get("SRS_MAIN_FILE_ENDPOINT")
srs_ids_ep = os.environ.get("SRS_IDS_ENDPOINT")

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    srs_database[srs_ids_collection].insert_one({
            "srs_id":srs_id,
            "srs_title":srs_title
        })
    response_body = {
        "message": "text srs added successfully",
        "srs_id": srs_id
    }

    return response_body

@app.post(srs_main_file_ep, status_code=201)
async def add_srs_text(file: UploadFile = File(...)):
    # ufile = file
    # srs_title = srs_data.srs_title
    # Handle the uploaded file here
    # You can save the file, process it, etc.
    # For example, to save it to a specific location:
    with open('uploads/'+file.filename, "wb") as f:
        f.write(await file.read())
    return {
            'message': 'file srs added successfully',
            'srs_title':file.filename
            }

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

@app.get(srs_ids_ep)
async def get_srs_ids():
    try:
        srs_ids_cursor = srs_database[srs_main_collection].find()
        srs_ids = [{
            'srs_id':str(srs_ids["_id"]),
            'srs_title':str(srs_ids["srs_title"])
            } for srs_ids in srs_ids_cursor]
        
        if srs_ids:

            response_body = {
                "message": "ids found and sent successfully",
                "srs_ids": srs_ids
            }
            
            return response_body
        else:
            raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": "SRS not found."})
    except Exception as e:
        raise HTTPException(status_code=400, detail="error in file srs sending", headers={"X-Error": str(e)})
