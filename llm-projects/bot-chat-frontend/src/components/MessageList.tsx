import React from 'react'
import Message from './Message'
import type { Message as MessageType } from '@/types'
import './MessageList.css'

interface MessageListProps {
  messages: MessageType[]
}

function MessageList({ messages }: MessageListProps): JSX.Element {
  if (messages.length === 0) {
    return (
      <div className="MessageList MessageList-empty">
        <p>Start a conversation by sending a message below.</p>
      </div>
    )
  }

  return (
    <div className="MessageList">
      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}
    </div>
  )
}

export default MessageList

