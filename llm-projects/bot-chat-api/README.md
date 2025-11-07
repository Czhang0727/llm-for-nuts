# Bot Chat API

FastAPI server for 1:1 chat bot conversations with LLM integration.

## Features

- FastAPI-based REST API
- Support for OpenAI and Dashscope (Qwen) LLM providers
- Session management for conversation history
- CORS enabled for frontend integration
- Auto-generated API documentation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

Create and initialize the SQLite database:

```bash
./create_db.sh
```

This will create the database at `data/chat.db` with all necessary tables and indexes.

**Options:**
- `--path PATH`: Specify custom database path
- `--force`: Overwrite existing database
- `--verify`: Verify existing database instead of creating new one
- `--help`: Show help message

**Examples:**
```bash
# Create database with default path
./create_db.sh

# Create database at custom path
./create_db.sh --path data/custom.db

# Overwrite existing database
./create_db.sh --force

# Verify existing database
./create_db.sh --verify
```

**Note:** You can also use the Python script directly: `python create_db.py`

### 3. Configure Environment Variables

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `LLM_PROVIDER`: Choose `"openai"` or `"dashscope"`
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)
- `DASHSCOPE_API_KEY`: Your Dashscope API key (if using Dashscope)
- `DATABASE_PATH`: Path to database file (default: `data/chat.db`)

### 4. Run the Server

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check

```http
GET /api/health
```

Returns server health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "bot-chat-api"
}
```

### Create Session

```http
POST /api/chat/session
```

Creates a new chat session.

**Response:**
```json
{
  "session_id": "uuid-string"
}
```

### Send Message

```http
POST /api/chat
```

Send a message to the bot and get a response.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I'm doing well, thank you! How can I help you today?",
  "session_id": "session-id"
}
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## Architecture

```
app.py              # Main FastAPI application
config.py           # Configuration management
session_manager.py  # Session and conversation history management
llm_service.py      # LLM provider integration (OpenAI/Dashscope)
chat_handler.py     # Chat logic and message processing
```

## Configuration

All configuration is done through environment variables (see `.env.example`):

- `API_HOST`: Server host (default: `0.0.0.0`)
- `API_PORT`: Server port (default: `5000`)
- `LLM_PROVIDER`: `"openai"` or `"dashscope"`
- `OPENAI_API_KEY`: OpenAI API key
- `DASHSCOPE_API_KEY`: Dashscope API key
- `OPENAI_MODEL`: OpenAI model name (default: `gpt-3.5-turbo`)
- `DASHSCOPE_MODEL`: Dashscope model name (default: `qwen-turbo`)
- `MAX_HISTORY_LENGTH`: Maximum messages to keep in context (default: `20`)

## Session Management

Sessions are stored in-memory by default. Each session maintains conversation history for context-aware responses. Sessions are identified by UUIDs.

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `404`: Session not found
- `500`: Server error

Error responses include a `detail` field with error information.

## Development

### Running in Development Mode

```bash
uvicorn app:app --reload
```

### Testing with curl

```bash
# Health check
curl http://localhost:5000/api/health

# Create session
curl -X POST http://localhost:5000/api/chat/session

# Send message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "your-session-id"}'
```

## Integration with Frontend

This API is designed to work with the React frontend in `bot-chat-frontend`. The frontend expects:

- Base URL: `http://localhost:5000/api`
- CORS enabled (already configured)
- Endpoints: `/health`, `/chat/session`, `/chat`

## Future Enhancements

- [ ] Database persistence for sessions
- [ ] Streaming responses
- [ ] Rate limiting
- [ ] User authentication
- [ ] Message export
- [ ] Multiple conversation contexts

