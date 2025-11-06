import React from 'react'
import type { Message as MessageType } from '@/types'
import './Message.css'

interface MessageProps {
  message: MessageType
}

function Message({ message }: MessageProps): JSX.Element {
  const isUser = message.role === 'user'
  const timestamp = message.timestamp
    ? new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : ''

  return (
    <div className={`Message Message-${isUser ? 'user' : 'bot'}`}>
      <div className="Message-content">
        <div className="Message-text">{message.content}</div>
        {timestamp && <div className="Message-timestamp">{timestamp}</div>}
      </div>
    </div>
  )
}

export default Message

