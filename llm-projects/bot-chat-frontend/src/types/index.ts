export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface ChatResponse {
  response: string
  session_id: string
}

