"""
FastAPI Server for YuvaSaarthi
Connects Next.js frontend to Python backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from loguru import logger

from backend.chatbot_engine import get_chatbot
from utils.indian_languages import SUPPORTED_INDIAN_LANGUAGES

# Initialize FastAPI app
app = FastAPI(
    title="YuvaSaarthi API",
    description="National Education Assistant for India - Backend API",
    version="2.0.0"
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
try:
    chatbot = get_chatbot()
    logger.info("Chatbot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize chatbot: {e}")
    chatbot = None


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    conversation_id: str = "default"
    include_videos: bool = True
    socratic_mode: bool = False
    teach_back: bool = False
    native_mnemonics: bool = False


class ChatResponse(BaseModel):
    response: str
    videos: List[Dict] = []
    language: str = "en"
    detected_language: Optional[str] = None


class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str


# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "YuvaSaarthi API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/api/chat",
            "languages": "/api/languages",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    try:
        health = chatbot.get_system_health()
        return {
            "status": "healthy",
            "components": health
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/languages", response_model=List[LanguageInfo])
async def get_languages():
    """Get list of supported languages"""
    languages = []
    for code, info in SUPPORTED_INDIAN_LANGUAGES.items():
        languages.append(LanguageInfo(
            code=code,
            name=info["name"],
            native_name=info["native_name"]
        ))
    return languages


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process chat message and return response
    
    - **message**: User's question/message
    - **language**: Language code (en, hi, ta, etc.)
    - **conversation_id**: Unique ID for user/session
    - **include_videos**: Whether to include YouTube video recommendations
    """
    if not chatbot:
        raise HTTPException(
            status_code=503,
            detail="Chatbot service is not available. Please check if vector store is initialized."
        )
    
    try:
        # Process the query through chatbot
        result = chatbot.process_query(
            query=request.message,
            user_id=request.conversation_id,
            language=request.language,
            include_videos=request.include_videos,
            socratic_mode=request.socratic_mode,
            teach_back=request.teach_back,
            native_mnemonics=request.native_mnemonics
        )
        
        return ChatResponse(
            response=result["response"],
            videos=result.get("videos", []),
            language=request.language,
            detected_language=result.get("detected_language")
        )
    
    except Exception as e:
        logger.error(f"Chat processing error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )


@app.post("/api/clear-history")
async def clear_history(conversation_id: str):
    """Clear conversation history for a user"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    try:
        chatbot.clear_history(conversation_id)
        return {"status": "success", "message": "History cleared"}
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "supported_languages": len(SUPPORTED_INDIAN_LANGUAGES),
        "chatbot_initialized": chatbot is not None,
        "version": "2.0.0"
    }


if __name__ == "__main__":
    logger.info("Starting YuvaSaarthi API Server...")
    logger.info("Frontend can connect at: http://localhost:8000")
    logger.info("API documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
