"""
Database manager for SQLite storage
"""
import sqlite3
from typing import Optional, List, Dict
from datetime import datetime
from pathlib import Path
from config import settings


class DatabaseManager:
    """Manages SQLite database operations for sessions and messages"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file. Defaults to settings.DATABASE_PATH
        """
        self.db_path = db_path or settings.DATABASE_PATH
        
        # Create data directory if it doesn't exist
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize schema
        self.initialize_schema()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def initialize_schema(self):
        """Initialize database schema (create tables if they don't exist)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Create sessions table (simplified: only id and title)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    title TEXT
                )
            """)
            
            # Create messages table (simplified: session_id, id, content, timestamp)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session_id 
                ON messages(session_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_timestamp 
                ON messages(timestamp)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session_timestamp 
                ON messages(session_id, timestamp)
            """)
            
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Database initialization error: {str(e)}")
        finally:
            conn.close()
    
    def create_session(self, session_id: str, title: Optional[str] = None) -> Dict:
        """
        Create a new chat session
        
        Args:
            session_id: Unique session identifier (UUID)
            title: Optional session title
            
        Returns:
            Dictionary with session data
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO sessions (id, title)
                VALUES (?, ?)
            """, (session_id, title))
            
            conn.commit()
            
            return {
                "id": session_id,
                "title": title
            }
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError(f"Session {session_id} already exists")
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Database error creating session: {str(e)}")
        finally:
            conn.close()
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get a session by ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with session data, or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, title
                FROM sessions
                WHERE id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "title": row["title"]
                }
            return None
        except sqlite3.Error as e:
            raise Exception(f"Database error getting session: {str(e)}")
        finally:
            conn.close()
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and all its messages
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session was deleted, False if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if session exists
            cursor.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
            if not cursor.fetchone():
                return False
            
            # Delete session (messages will be cascade deleted)
            cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            conn.commit()
            
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Database error deleting session: {str(e)}")
        finally:
            conn.close()
    
    def add_message(self, session_id: str, content: str) -> int:
        """
        Add a message to a session
        
        Args:
            session_id: Session identifier
            content: Message content
            
        Returns:
            Message ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verify session exists
            cursor.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
            if not cursor.fetchone():
                raise ValueError(f"Session {session_id} does not exist")
            
            # Insert message
            cursor.execute("""
                INSERT INTO messages (session_id, content, timestamp)
                VALUES (?, ?, ?)
            """, (session_id, content, datetime.utcnow().isoformat()))
            
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Database error adding message: {str(e)}")
        finally:
            conn.close()
    
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Get messages for a session
        
        Args:
            session_id: Session identifier
            limit: Optional limit on number of messages to return
            
        Returns:
            List of message dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            query = """
                SELECT id, session_id, content, timestamp
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp ASC
            """
            
            if limit:
                query += " LIMIT ?"
                cursor.execute(query, (session_id, limit))
            else:
                cursor.execute(query, (session_id,))
            
            rows = cursor.fetchall()
            messages = []
            for row in rows:
                messages.append({
                    "id": row["id"],
                    "session_id": row["session_id"],
                    "content": row["content"],
                    "timestamp": row["timestamp"]
                })
            
            return messages
        except sqlite3.Error as e:
            raise Exception(f"Database error getting messages: {str(e)}")
        finally:
            conn.close()
    

