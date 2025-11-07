"""
Data models for chat application
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============================================================================
# Database Models (Internal)
# ============================================================================

class Session(BaseModel):
    """Session data model"""
    id: str = Field(..., description="Unique session identifier (UUID)")
    title: Optional[str] = Field(None, description="Optional session title")


class Message(BaseModel):
    """Message data model"""
    id: Optional[int] = Field(None, description="Message ID (auto-increment)")
    session_id: str = Field(..., description="Session identifier")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO format timestamp")


# ============================================================================
# API Request Models
# ============================================================================

class CreateSessionRequest(BaseModel):
    """Request to create a new session"""
    title: Optional[str] = Field(None, description="Optional session title")


class ChatRequest(BaseModel):
    """Request to send a chat message"""
    message: str = Field(..., description="User's message", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID (creates new if not provided)")


# ============================================================================
# API Response Models
# ============================================================================

class SessionResponse(BaseModel):
    """Response for session creation"""
    session_id: str = Field(..., description="Created session ID")
    title: Optional[str] = Field(None, description="Session title")


class ChatResponse(BaseModel):
    """Response for chat message"""
    response: str = Field(..., description="Bot's response")
    session_id: str = Field(..., description="Session ID")
    message_id: Optional[int] = Field(None, description="Message ID of the bot's response")


class MessageResponse(BaseModel):
    """Response for a single message"""
    id: int = Field(..., description="Message ID")
    session_id: str = Field(..., description="Session ID")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO format timestamp")


class SessionHistoryResponse(BaseModel):
    """Response for session history"""
    session_id: str = Field(..., description="Session ID")
    title: Optional[str] = Field(None, description="Session title")
    messages: List[MessageResponse] = Field(default_factory=list, description="List of messages")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    service: str = Field(default="bot-chat-api", description="Service name")
    database: Optional[str] = Field(None, description="Database connection status")


# ============================================================================
# Internal Data Structures
# ============================================================================

class ChatHistory(BaseModel):
    """Internal structure for chat history"""
    session_id: str
    messages: List[Message] = Field(default_factory=list)
    
    def add_message(self, content: str) -> Message:
        """Add a new message to history"""
        message = Message(
            session_id=self.session_id,
            content=content,
            timestamp=datetime.utcnow().isoformat()
        )
        self.messages.append(message)
        return message
    
    def to_list(self) -> List[dict]:
        """Convert to list of dictionaries for LLM processing"""
        return [
            {
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in self.messages
        ]


class ChatContext(BaseModel):
    """Context for a chat conversation"""
    session: Session
    history: ChatHistory
    current_message: Optional[str] = None
    
    def get_conversation_context(self) -> List[dict]:
        """Get conversation context for LLM"""
        context = []
        for msg in self.history.messages:
            context.append({
                "content": msg.content,
                "timestamp": msg.timestamp
            })
        if self.current_message:
            context.append({
                "content": self.current_message,
                "timestamp": datetime.utcnow().isoformat()
            })
        return context

