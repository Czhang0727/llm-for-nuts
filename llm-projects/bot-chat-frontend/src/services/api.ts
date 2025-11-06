import axios from 'axios'
import type { ChatResponse } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Create a new chat session
 * @returns {Promise<string>} Session ID
 */
export async function createSession(): Promise<string> {
  try {
    const response = await api.post<{ session_id: string }>('/chat/session')
    return response.data.session_id
  } catch (error) {
    console.error('Error creating session:', error)
    throw new Error('Failed to create chat session')
  }
}

/**
 * Send a message to the bot
 * @param {string} message - The user's message
 * @param {string} sessionId - The current session ID
 * @returns {Promise<ChatResponse>}
 */
export async function sendMessage(message: string, sessionId: string): Promise<ChatResponse> {
  try {
    const response = await api.post<ChatResponse>('/chat', {
      message,
      session_id: sessionId,
    })
    return response.data
  } catch (error) {
    console.error('Error sending message:', error)
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.error || 'Failed to send message')
    }
    throw new Error('Network error. Please check if the backend is running.')
  }
}

/**
 * Health check endpoint
 * @returns {Promise<boolean>}
 */
export async function healthCheck(): Promise<boolean> {
  try {
    const response = await api.get('/health')
    return response.status === 200
  } catch (error) {
    return false
  }
}

