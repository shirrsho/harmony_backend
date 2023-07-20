from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mongodb import MongoDB
import os
from dotenv import load_dotenv

load_dotenv()

database_name = os.environ.get("DATABASE_NAME")
srs_main_ep = os.environ.get("POST_SRS_MAIN_ENDPOINT")
srs_main_collection = os.environ.get("SRS_MAIN_COLLECTION")

app = FastAPI()

mongodb = MongoDB()
srs_database = mongodb.get_client()[database_name]

class SRSData(BaseModel):
    text: str

@app.post(srs_main_ep, status_code=201)
async def add_srs_text(srs_data: SRSData):
    text = srs_data.text
    if not text:
        raise HTTPException(status_code=400, detail="error in text srs adding", headers={"X-Error": "Text cannot be empty."})

    # Insert the SRS data into the MongoDB collection.
    result = srs_database[srs_main_collection].insert_one({"text": text})
    srs_id = str(result.inserted_id)

    response_body = {
        "message": "text srs added successfully",
        "srs_id": srs_id
    }

    return response_body
