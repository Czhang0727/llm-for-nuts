"""
Session management for chat conversations
"""
import uuid
from typing import List, Dict, Optional
from datetime import datetime


class SessionManager:
    """Manages chat sessions and conversation history"""
    
    def __init__(self):
        """Initialize session manager with in-memory storage"""
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
    
    def create_session(self) -> str:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        return session_id
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists"""
        return session_id in self.sessions
    
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a session"""
        if not self.session_exists(session_id):
            return []
        return self.sessions[session_id].copy()
    
    def add_message(self, session_id: str, content: str):
        """Add a message to the session history"""
        if not self.session_exists(session_id):
            raise ValueError(f"Session {session_id} does not exist")
        
        message = {
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.sessions[session_id].append(message)
    
    def clear_session(self, session_id: str):
        """Clear all messages from a session"""
        if self.session_exists(session_id):
            self.sessions[session_id] = []
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if self.session_exists(session_id):
            del self.sessions[session_id]

