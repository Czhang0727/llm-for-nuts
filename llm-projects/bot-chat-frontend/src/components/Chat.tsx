import React, { useState, useEffect, useRef } from 'react'
import MessageList from './MessageList'
import Compose from './Compose'
import SendButton from './SendButton'
import { sendMessage, createSession } from '@/services/api'
import type { Message } from '@/types'
import './Chat.css'

function Chat(): JSX.Element {
  const [messages, setMessages] = useState<Message[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [isInitializing, setIsInitializing] = useState<boolean>(true)
  const [inputValue, setInputValue] = useState<string>('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize session on mount
  useEffect(() => {
    const initializeSession = async (): Promise<void> => {
      setIsInitializing(true)
      setError(null)
      try {
        const newSessionId = await createSession()
        setSessionId(newSessionId)
        setError(null)
      } catch (err) {
        setError(
          'Backend API not available. Please make sure the backend server is running on http://localhost:5000'
        )
        console.error('Session initialization error:', err)
        // Allow typing even without session - we'll try to create session when sending
      } finally {
        setIsInitializing(false)
      }
    }
    initializeSession()
  }, [])

  const handleSend = async (): Promise<void> => {
    if (!inputValue.trim() || isLoading) return

    // Try to create session if we don't have one
    let currentSessionId = sessionId
    if (!currentSessionId) {
      try {
        setIsLoading(true)
        setError(null)
        currentSessionId = await createSession()
        setSessionId(currentSessionId)
      } catch (err) {
        setError(
          'Cannot connect to backend API. Please make sure the backend server is running on http://localhost:5000'
        )
        setIsLoading(false)
        return
      }
    }

    const userMessage: Message = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    }

    // Add user message immediately
    setMessages((prev) => [...prev, userMessage])
    const messageText = inputValue
    setInputValue('')
    setIsLoading(true)
    setError(null)

    try {
      const response = await sendMessage(messageText, currentSessionId)

      const botMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (err) {
      setError('Failed to send message. Please check if the backend API is running.')
      console.error('Send message error:', err)
      // Remove user message if send failed
      setMessages((prev) => prev.filter((msg) => msg !== userMessage))
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="Chat">
      <div className="Chat-container">
        <MessageList messages={messages} />
        {isLoading && (
          <div className="Chat-loading">
            <div className="Chat-loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>Bot is typing...</p>
          </div>
        )}
        {error && <div className="Chat-error">{error}</div>}
        <div ref={messagesEndRef} />
      </div>
      <div className="Chat-input-area">
        <Compose
          value={inputValue}
          onChange={setInputValue}
          onKeyPress={handleKeyPress}
          disabled={isLoading || isInitializing}
        />
        <SendButton
          onClick={handleSend}
          disabled={isLoading || isInitializing || !inputValue.trim()}
        />
      </div>
    </div>
  )
}

export default Chat

