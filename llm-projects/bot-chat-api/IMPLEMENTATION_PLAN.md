# Bot Chat Implementation Plan

## Overview
Create a 1:1 chat bot system with:
- **Backend API**: Python Flask/FastAPI server for handling chat requests
- **Frontend**: Simple web interface or CLI for chatting with the bot
- **LLM Integration**: Connect with OpenAI or Dashscope API for bot responses

## Frontend Options

### Option A: Web Frontend with React.js (Selected)
- React.js single-page application
- Modern chat UI with message bubbles
- Component-based architecture
- Easy to extend and maintain

### Option B: CLI Application
- Command-line interface for chat
- Simple text-based interaction
- Good for testing and automation

### Option C: API Only
- Backend API only, no frontend
- Can be integrated with any client
- Useful for API-first approach

## Architecture

### Option A: Web Frontend
```
┌─────────────────────┐
│  Web Frontend       │
│  (HTML/CSS/JS)      │
│  - Chat UI          │
│  - Message Input    │
│  - Chat History     │
└──────────┬──────────┘
           │ HTTP Request
           ▼
┌─────────────────────┐
│  Bot Chat API       │
│  (Backend)          │
│  - Flask/FastAPI    │
│  - Message Handler  │
│  - Session Manager  │
└──────────┬──────────┘
           │ API Call
           ▼
┌─────────────────────┐
│  LLM Service        │
│  (OpenAI/Dashscope) │
│  - Chat Completion  │
│  - Response Gen     │
└─────────────────────┘
```

### Option B: CLI Application
```
┌─────────────────────┐
│  CLI Chat Client    │
│  (Python)           │
│  - Input/Output     │
│  - API Calls        │
└──────────┬──────────┘
           │ HTTP Request
           ▼
┌─────────────────────┐
│  Bot Chat API       │
│  (Backend)          │
└──────────┬──────────┘
           │ API Call
           ▼
┌─────────────────────┐
│  LLM Service        │
└─────────────────────┘
```

## Backend Design Document

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   API Layer  │  │  Chat Handler│  │ Session Mgr  │     │
│  │  (app.py)    │→ │              │→ │              │     │
│  └──────────────┘  └──────────────┘  └──────┬───────┘     │
│                                              │              │
│  ┌──────────────┐  ┌──────────────┐         │              │
│  │  LLM Service│  │  DB Manager   │←────────┘              │
│  │             │  │  (SQLite)     │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema (SQLite)

#### Sessions Table
Stores chat session information.

```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,                    -- UUID session identifier
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title TEXT,                             -- Optional session title
    metadata TEXT                            -- JSON metadata (future use)
);

CREATE INDEX idx_sessions_created_at ON sessions(created_at);
CREATE INDEX idx_sessions_updated_at ON sessions(updated_at);
```

#### Messages Table
Stores all messages (both user and assistant) with session relationship.

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,               -- Foreign key to sessions
    role TEXT NOT NULL,                     -- 'user' or 'assistant'
    content TEXT NOT NULL,                  -- Message content
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,                          -- JSON metadata (future use)
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_messages_session_timestamp ON messages(session_id, timestamp);
```

### Chat Data Structure Design

#### Database Models (Internal)

**Session Model:**
```python
class Session:
    id: str                    # UUID (PRIMARY KEY)
    title: Optional[str]       # Optional session title
```

**Message Model:**
```python
class Message:
    id: Optional[int]           # Auto-increment ID (PRIMARY KEY)
    session_id: str             # Foreign key to sessions
    content: str                # Message content
    timestamp: str              # ISO format timestamp
```

#### API Request/Response Models

**Create Session Request:**
```python
class CreateSessionRequest:
    title: Optional[str]        # Optional session title
```

**Create Session Response:**
```python
class SessionResponse:
    session_id: str            # Created session ID
    title: Optional[str]       # Session title
```

**Chat Request:**
```python
class ChatRequest:
    message: str               # User's message (required)
    session_id: Optional[str]  # Session ID (optional, creates new if not provided)
```

**Chat Response:**
```python
class ChatResponse:
    response: str              # Bot's response
    session_id: str           # Session ID
    message_id: Optional[int]  # Message ID of bot's response
```

**Message Response:**
```python
class MessageResponse:
    id: int                    # Message ID
    session_id: str           # Session ID
    content: str              # Message content
    timestamp: str           # ISO format timestamp
```

**Session History Response:**
```python
class SessionHistoryResponse:
    session_id: str           # Session ID
    title: Optional[str]     # Session title
    messages: List[MessageResponse]  # List of messages
```

#### Internal Data Structures

**ChatHistory:**
```python
class ChatHistory:
    session_id: str
    messages: List[Message]
    
    def add_message(content: str) -> Message
    def to_list() -> List[dict]  # For LLM processing
```

**ChatContext:**
```python
class ChatContext:
    session: Session
    history: ChatHistory
    current_message: Optional[str]
    
    def get_conversation_context() -> List[dict]
```

#### Data Flow Structure

```
User Message → ChatRequest
    ↓
Session Lookup/Creation
    ↓
ChatContext (session + history + current_message)
    ↓
ChatHandler.get_response(message, history)
    ↓
LLM Service (processes context)
    ↓
Bot Response → ChatResponse
    ↓
Save to Database (session + messages)
```

#### Message Format Examples

**Database Storage:**
```json
// Session
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "My Chat Session"
}

// Message
{
  "id": 1,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "content": "Hello, how are you?",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**API Request/Response:**
```json
// POST /api/chat
Request:
{
  "message": "Hello, how are you?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}

Response:
{
  "response": "Hello, World!",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": 2
}
```

**History Retrieval:**
```json
// GET /api/chat/session/{session_id}/history
Response:
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "My Chat Session",
  "messages": [
    {
      "id": 1,
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "content": "Hello, how are you?",
      "timestamp": "2024-01-01T12:00:00.000Z"
    },
    {
      "id": 2,
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "content": "Hello, World!",
      "timestamp": "2024-01-01T12:00:01.000Z"
    }
  ]
}
```

#### Key Design Decisions

1. **Simplified Schema**: Removed `role`, `metadata`, `created_at`, `updated_at` for simplicity
2. **Message Ordering**: Messages are ordered by `timestamp` ASC for chronological conversation flow
3. **Session Management**: Sessions are identified by UUID, allowing easy creation and lookup
4. **History Context**: History is passed as a list of message dictionaries to LLM service
5. **Type Safety**: Using Pydantic models for validation and type checking
6. **Flexible Titles**: Session titles are optional, can be set at creation or updated later

### API Endpoints Design

#### 1. Health Check
```http
GET /api/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "bot-chat-api",
  "database": "connected"
}
```

#### 2. Create Session
```http
POST /api/chat/session
```
**Request Body:** (optional)
```json
{
  "title": "Optional session title"
}
```
**Response:**
```json
{
  "session_id": "uuid-string",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 3. Send Message
```http
POST /api/chat
```
**Request Body:**
```json
{
  "message": "User message text",
  "session_id": "uuid-string"  // Optional, creates new if not provided
}
```
**Response:**
```json
{
  "response": "Bot response text",
  "session_id": "uuid-string",
  "message_id": 123
}
```

#### 4. Get Session History (Future)
```http
GET /api/chat/session/{session_id}/history
```
**Response:**
```json
{
  "session_id": "uuid-string",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Hello, World!",
      "timestamp": "2024-01-01T00:00:01Z"
    }
  ]
}
```

#### 5. List Sessions (Future)
```http
GET /api/chat/sessions
```
**Query Parameters:**
- `limit`: Number of sessions to return (default: 20)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "sessions": [
    {
      "id": "uuid-string",
      "title": "Session title",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "message_count": 10
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

#### 6. Delete Session (Future)
```http
DELETE /api/chat/session/{session_id}
```
**Response:**
```json
{
  "success": true,
  "message": "Session deleted"
}
```

### Component Design

#### 1. Database Manager (`database.py`)
**Responsibilities:**
- Database connection management
- Schema initialization and migrations
- CRUD operations for sessions and messages
- Connection pooling and transaction management

**Key Methods:**
```python
class DatabaseManager:
    def __init__(self, db_path: str)
    def initialize_schema(self)
    def create_session(self, session_id: str, title: Optional[str] = None) -> Session
    def get_session(self, session_id: str) -> Optional[Session]
    def add_message(self, session_id: str, role: str, content: str) -> Message
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[Message]
    def update_session_timestamp(self, session_id: str)
    def delete_session(self, session_id: str)
    def list_sessions(self, limit: int = 20, offset: int = 0) -> List[Session]
```

#### 2. Session Manager (`session_manager.py`)
**Responsibilities:**
- Session lifecycle management
- Message history retrieval
- Integration with database manager

**Key Methods:**
```python
class SessionManager:
    def __init__(self, db_manager: DatabaseManager)
    def create_session(self, title: Optional[str] = None) -> str
    def session_exists(self, session_id: str) -> bool
    def get_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict]
    def add_message(self, session_id: str, role: str, content: str)
    def delete_session(self, session_id: str)
```

#### 3. Chat Handler (`chat_handler.py`)
**Responsibilities:**
- Message processing logic
- LLM integration coordination
- Response generation

**Key Methods:**
```python
class ChatHandler:
    def __init__(self, llm_service: LLMService)
    async def get_response(self, message: str, history: List[Dict]) -> str
    def _prepare_messages(self, current_message: str, history: List[Dict]) -> List[Dict]
```

#### 4. LLM Service (`llm_service.py`)
**Responsibilities:**
- LLM provider abstraction
- API calls to OpenAI/Dashscope
- Error handling and retries

**Key Methods:**
```python
class LLMService:
    def __init__(self, provider: str, api_key: str, model: str)
    async def get_completion(self, messages: List[Dict]) -> str
```

### Data Flow

#### Message Send Flow
```
1. Client → POST /api/chat
   {
     "message": "Hello",
     "session_id": "uuid" (optional)
   }

2. API Layer (app.py)
   - Validates request
   - Checks/creates session

3. Session Manager
   - Retrieves conversation history from DB
   - Returns message list

4. Chat Handler
   - Prepares messages for LLM
   - Calls LLM Service

5. LLM Service
   - Makes API call to OpenAI/Dashscope
   - Returns generated response

6. Database Manager
   - Saves user message to DB
   - Saves assistant response to DB
   - Updates session timestamp

7. API Layer
   - Returns response to client
   {
     "response": "Hello, World!",
     "session_id": "uuid",
     "message_id": 123
   }
```

### Error Handling

#### Error Response Format
```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "status_code": 400
}
```

#### Error Types
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Session not found
- **500 Internal Server Error**: Server/database errors
- **503 Service Unavailable**: LLM service unavailable

#### Error Handling Strategy
1. **Input Validation**: Use Pydantic models for request validation
2. **Database Errors**: Catch SQLite exceptions and return appropriate HTTP status
3. **LLM Errors**: Handle API rate limits, timeouts, and errors gracefully
4. **Logging**: Log all errors with context for debugging

### Configuration

#### Database Configuration
```python
# config.py
DATABASE_PATH: str = "data/chat.db"  # SQLite database file path
DATABASE_BACKUP_ENABLED: bool = True
DATABASE_BACKUP_INTERVAL: int = 3600  # seconds
```

#### Environment Variables
```bash
# Database
DATABASE_PATH=data/chat.db

# API
API_HOST=0.0.0.0
API_PORT=5000

# LLM
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
DASHSCOPE_API_KEY=your_key
OPENAI_MODEL=gpt-3.5-turbo
DASHSCOPE_MODEL=qwen-turbo

# Chat
MAX_HISTORY_LENGTH=20
```

### File Structure (Updated)

```
llm-projects/
└── bot-chat-api/
    ├── app.py                 # Main FastAPI application
    ├── config.py              # Configuration management
    ├── database.py            # Database manager (SQLite)
    ├── models.py              # Pydantic data models
    ├── chat_handler.py        # Chat logic
    ├── llm_service.py         # LLM integration
    ├── session_manager.py     # Session management
    ├── requirements.txt       # Python dependencies
    ├── .env.example           # Environment variables template
    ├── README.md              # API documentation
    └── data/                  # Database directory
        └── chat.db            # SQLite database file
```

### Database Migration Strategy

#### Initial Schema
- Create `sessions` and `messages` tables on first run
- Use SQLite's schema versioning for future migrations

#### Migration Script
```python
# migrations.py
def migrate_database(db_path: str):
    # Check current schema version
    # Apply migrations if needed
    # Update schema version
```

### Performance Considerations

1. **Database Indexing**: Indexes on `session_id`, `timestamp` for fast queries
2. **Connection Pooling**: SQLite connection reuse
3. **Query Optimization**: Limit message history retrieval to recent messages
4. **Caching**: Consider caching recent sessions in memory (optional)

### Security Considerations

1. **Input Sanitization**: Validate and sanitize all user inputs
2. **SQL Injection Prevention**: Use parameterized queries
3. **Rate Limiting**: Implement rate limiting per session/IP (future)
4. **Data Privacy**: Ensure message content is stored securely
5. **CORS**: Configure CORS appropriately for production

### Testing Strategy

1. **Unit Tests**: Test each component independently
2. **Integration Tests**: Test database operations and API endpoints
3. **End-to-End Tests**: Test complete message flow
4. **Database Tests**: Use in-memory SQLite for testing

## Implementation Steps

### Phase 1: Backend API (bot-chat-api)

#### 1.1 Project Setup
- [ ] Create Flask/FastAPI application structure
- [ ] Set up requirements.txt with dependencies (flask, openai, dashscope)
- [ ] Create configuration file for API keys and settings
- [ ] Set up environment variables handling

#### 1.2 Core API Endpoints
- [ ] `POST /api/chat` - Send message and get bot response
  - Input: `{ "message": "user message", "session_id": "optional" }`
  - Output: `{ "response": "bot response", "session_id": "session_id" }`
- [ ] `POST /api/chat/session` - Create new chat session
  - Output: `{ "session_id": "new_session_id" }`
- [ ] `GET /api/health` - Health check endpoint

#### 1.3 Chat Logic
- [ ] Implement message handler
- [ ] Session management (store conversation history)
- [ ] LLM integration (OpenAI or Dashscope)
- [ ] Error handling and response formatting
- [ ] Rate limiting (optional)

#### 1.4 Data Storage
- [ ] Create database manager (`database.py`)
- [ ] Implement SQLite schema (sessions and messages tables)
- [ ] Database initialization and migration logic
- [ ] Session storage with SQLite persistence
- [ ] Message storage with foreign key relationships
- [ ] Conversation history retrieval from database

### Phase 2: Frontend (Choose One Option)

#### Option A: Web Frontend with React.js

##### 2.1 React Project Setup
- [ ] Create React app structure
- [ ] Set up `package.json` with dependencies (react, react-dom, react-scripts)
- [ ] Configure build and development scripts
- [ ] Set up project structure

##### 2.2 React Components
- [ ] `App.js` - Main application component
- [ ] `Chat.js` - Main chat container component
- [ ] `MessageList.js` - Component for displaying messages
- [ ] `Message.js` - Individual message bubble component
- [ ] `MessageInput.js` - Input area with send button
- [ ] `LoadingIndicator.js` - Loading state component

##### 2.3 API Integration
- [ ] `services/api.js` - API service module
  - HTTP request wrapper (fetch/axios)
  - Error handling
  - Base URL configuration
  - Session management

##### 2.4 Styling
- [ ] `App.css` - Main app styles
- [ ] Component-specific CSS modules or styled components
- [ ] Message bubbles styling (user vs bot)
- [ ] Responsive layout
- [ ] Modern, clean design

#### Option B: CLI Application

##### 2.1 CLI Client
- [ ] `client.py` - Command-line chat client
  - Interactive input loop
  - API calls to backend
  - Pretty printing of messages
  - Session management
  - Exit command

#### Option C: API Only
- [ ] Skip frontend, focus on API
- [ ] Provide API documentation
- [ ] Create example curl requests

### Phase 3: Integration & Testing

#### 3.1 Backend Testing
- [ ] Test API endpoints
- [ ] Test LLM integration
- [ ] Test session management
- [ ] Test error handling

#### 3.2 Frontend Testing
- [ ] Test message sending
- [ ] Test message receiving
- [ ] Test UI interactions
- [ ] Test error states

#### 3.3 Integration Testing
- [ ] End-to-end chat flow
- [ ] Session persistence
- [ ] Network error handling

## Technical Decisions

### Backend Framework
- **Option A**: Flask (simpler, lighter)
- **Option B**: FastAPI (modern, async support, auto docs)
- **Recommendation**: FastAPI for better async support and auto-generated docs

### LLM Provider
- **Option A**: OpenAI (via `openai` SDK)
- **Option B**: Dashscope/Qwen (via `dashscope` SDK)
- **Recommendation**: Support both, configurable via environment variable

### Session Storage
- **Option A**: In-memory (simple, no persistence)
- **Option B**: File-based JSON (persistent, simple)
- **Option C**: Database (SQLite/PostgreSQL) ✅ **Selected**
- **Decision**: SQLite for local persistence, simple deployment, and reliable data storage

### Message Format
```json
{
  "role": "user|assistant",
  "content": "message text",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## File Structure

### Option A: Web Frontend with React.js
```
llm-projects/
├── bot-chat-api/              # Backend API
│   ├── app.py                 # Main FastAPI app
│   ├── config.py              # Configuration
│   ├── database.py            # Database manager (SQLite)
│   ├── models.py              # Pydantic data models
│   ├── chat_handler.py        # Chat logic
│   ├── llm_service.py         # LLM integration
│   ├── session_manager.py     # Session management
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── README.md              # API documentation
│   └── data/                  # Database directory
│       └── chat.db            # SQLite database file
│
└── bot-chat-frontend/         # React.js Frontend
    ├── package.json           # NPM dependencies
    ├── public/
    │   └── index.html         # HTML template
    ├── src/
    │   ├── App.js             # Main app component
    │   ├── App.css            # App styles
    │   ├── components/
    │   │   ├── Chat.js        # Chat container
    │   │   ├── MessageList.js # Message list
    │   │   ├── Message.js     # Message bubble
    │   │   ├── MessageInput.js # Input component
    │   │   └── LoadingIndicator.js
    │   └── services/
    │       └── api.js         # API service
    └── README.md              # Frontend documentation
```

### Option B: CLI Application
```
llm-projects/
└── bot-chat-api/
    ├── app.py                 # Main FastAPI app
    ├── config.py              # Configuration
    ├── database.py            # Database manager (SQLite)
    ├── models.py              # Pydantic data models
    ├── chat_handler.py        # Chat logic
    ├── llm_service.py         # LLM integration
    ├── session_manager.py     # Session management
    ├── client.py              # CLI chat client
    ├── requirements.txt       # Python dependencies
    ├── .env.example           # Environment variables template
    ├── README.md              # API documentation
    └── data/                  # Database directory
        └── chat.db            # SQLite database file
```

### Option C: API Only
```
llm-projects/
└── bot-chat-api/
    ├── app.py                 # Main FastAPI app
    ├── config.py              # Configuration
    ├── database.py            # Database manager (SQLite)
    ├── models.py              # Pydantic data models
    ├── chat_handler.py        # Chat logic
    ├── llm_service.py         # LLM integration
    ├── session_manager.py     # Session management
    ├── requirements.txt       # Python dependencies
    ├── .env.example           # Environment variables template
    ├── README.md              # API documentation
    └── data/                  # Database directory
        └── chat.db            # SQLite database file
```

## Dependencies

### Backend
- `fastapi` - Web framework ✅
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `openai` - OpenAI SDK (already in requirements.txt)
- `dashscope` - Dashscope SDK (already in requirements.txt)
- `python-dotenv` - Environment variables
- `aiosqlite` or `sqlite3` - SQLite database (built-in or async)

### Frontend (Option A: React.js)
- `react` - React library
- `react-dom` - React DOM rendering
- `react-scripts` or `vite` - Build tool and dev server
- `axios` (optional) - HTTP client (or use fetch)

### Frontend (Option B: CLI)
- `rich` (optional) - For pretty terminal output
- `prompt-toolkit` (optional) - For enhanced input handling

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - OpenAI API key
- `DASHSCOPE_API_KEY` - Dashscope API key
- `LLM_PROVIDER` - `openai` or `dashscope`
- `API_HOST` - Backend API host (default: `localhost:5000`)
- `API_PORT` - Backend API port (default: `5000`)

## Next Steps

1. **Decide on frontend approach** (Web, CLI, or API-only)
2. Start with Phase 1 (Backend API)
3. Test backend independently (using curl or Postman)
4. Move to Phase 2 (Frontend) based on chosen option
5. Integrate and test
6. Deploy and iterate

## Recommendation

**Option A (React.js Frontend)** provides:
- Component-based architecture for maintainability
- Modern React patterns and hooks
- Easy to extend with additional features
- Professional user interface
- Good development experience with hot reload

## Future Enhancements
- [ ] Multi-turn conversation context
- [ ] Message persistence (database)
- [ ] User authentication
- [ ] Rate limiting and quotas
- [ ] Streaming responses
- [ ] Typing indicators
- [ ] Message timestamps in UI
- [ ] Error retry mechanism
- [ ] Message history export

