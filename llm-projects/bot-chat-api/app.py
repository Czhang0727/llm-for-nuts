"""
FastAPI server for bot chat application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from config import settings
from chat_handler import ChatHandler
from session_manager import SessionManager
from database import DatabaseManager
from models import MessageResponse, SessionHistoryResponse

app = FastAPI(
    title="Bot Chat API",
    description="API for 1:1 chat bot conversations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
session_manager = SessionManager()
chat_handler = ChatHandler()
db_manager = DatabaseManager()


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


class SessionResponse(BaseModel):
    session_id: str


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "bot-chat-api"}


@app.post("/api/chat/session", response_model=SessionResponse)
async def create_session():
    """Create a new chat session"""
    session_id = session_manager.create_session()
    return SessionResponse(session_id=session_id)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and get bot response"""
    try:
        # Validate session
        if request.session_id:
            if not session_manager.session_exists(request.session_id):
                raise HTTPException(
                    status_code=404,
                    detail="Session not found"
                )
        else:
            # Create new session if not provided
            request.session_id = session_manager.create_session()
        
        # Get conversation history
        history = session_manager.get_history(request.session_id)
        
        # Get bot response
        bot_response = await chat_handler.get_response(
            message=request.message,
            history=history
        )
        
        # Add messages to history
        session_manager.add_message(request.session_id, request.message)
        session_manager.add_message(request.session_id, bot_response)
        
        return ChatResponse(
            response=bot_response,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )


@app.get("/api/chat/{chat_id}/messages", response_model=SessionHistoryResponse)
async def get_chat_messages(chat_id: str):
    """
    Get all messages for a chat session
    
    Args:
        chat_id: Session/chat identifier
        
    Returns:
        Session history with all messages
    """
    try:
        # Verify session exists
        session = db_manager.get_session(chat_id)
        if not session:
            raise HTTPException(
                status_code=404,
                detail=f"Chat session {chat_id} not found"
            )
        
        # Get all messages for the session
        messages_data = db_manager.get_messages(chat_id)
        
        # Convert to MessageResponse models
        messages = [
            MessageResponse(
                id=msg["id"],
                session_id=msg["session_id"],
                content=msg["content"],
                timestamp=msg["timestamp"]
            )
            for msg in messages_data
        ]
        
        return SessionHistoryResponse(
            session_id=chat_id,
            title=session.get("title"),
            messages=messages
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat messages: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )

