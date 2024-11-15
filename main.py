from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
import time
import logging

# Initialize the FastAPI app
app = FastAPI()

# Logger Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS Configuration
origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for users
users_db = []

# Middleware to log the time taken for each request
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url} completed in {process_time:.4f} seconds")
    return response

# Pydantic model for user input
class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    height: float

# POST endpoint to create a new user
@app.post("/users", status_code=201)
async def create_user(user: User):
    # Add user to in-memory database
    users_db.append(user.dict())
    return {"message": "User created successfully", "user": user.dict()}

# GET endpoint to fetch all users (optional)
@app.get("/users", status_code=200)
async def get_users():
    return users_db
