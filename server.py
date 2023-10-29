import atexit
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from mongodb import MongoDB

from routes.api import router as api_router
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    # Close the MongoDB connection when the FastAPI server is shutting down
    MongoDB().get_client().close()
    print("Shutting down MongoDB")

# Register a function to close the MongoDB connection on process exit
def close_mongodb_connection():
    MongoDB().get_client().close()
    print("MongoDB connection closed")

# Register the function to be called on process exit
atexit.register(close_mongodb_connection)

app.include_router(api_router)