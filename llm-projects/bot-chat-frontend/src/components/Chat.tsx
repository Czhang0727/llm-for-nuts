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
      try {
        const newSessionId = await createSession()
        setSessionId(newSessionId)
      } catch (err) {
        setError('Failed to initialize chat session')
        console.error('Session initialization error:', err)
      }
    }
    initializeSession()
  }, [])

  const handleSend = async (): Promise<void> => {
    if (!inputValue.trim() || !sessionId || isLoading) return

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
      const response = await sendMessage(messageText, sessionId)

      const botMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (err) {
      setError('Failed to send message. Please try again.')
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
          disabled={isLoading || !sessionId}
        />
        <SendButton
          onClick={handleSend}
          disabled={isLoading || !sessionId || !inputValue.trim()}
        />
      </div>
    </div>
  )
}

export default Chat

