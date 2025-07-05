from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from .generator import QuizGenerator
from .schemas import QuizRequest, QuizResponse, Question
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for local testing)
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()

# Load configuration
try:
    with open('config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    raise RuntimeError("config.json is missing")

# Initialize generator
generator = QuizGenerator(config)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str

class VersionResponse(BaseModel):
    version: str
    generator_mode: str
    supported_difficulties: List[str]
    supported_types: List[str]

@app.post("/generate", response_model=QuizResponse)
async def generate_quiz(quiz_request: QuizRequest):
    """Generate quiz questions based on goal and parameters"""
    return generator.generate_quiz(quiz_request)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/version", response_model=VersionResponse)
async def version_info():
    """Return version and configuration information"""
    return {
        "version": config["version"],
        "generator_mode": config["generator_mode"],
        "supported_difficulties": config["supported_difficulties"],
        "supported_types": config["supported_types"]
    }