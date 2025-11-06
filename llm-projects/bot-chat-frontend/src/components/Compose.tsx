import React from 'react'
import './Compose.css'

interface ComposeProps {
  value: string
  onChange: (value: string) => void
  onKeyPress: (e: React.KeyboardEvent<HTMLInputElement>) => void
  disabled: boolean
}

function Compose({ value, onChange, onKeyPress, disabled }: ComposeProps): JSX.Element {
  return (
    <input
      type="text"
      className="Compose"
      placeholder={disabled ? 'Connecting...' : 'Type your message...'}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onKeyPress={onKeyPress}
      disabled={disabled}
    />
  )
}

export default Compose

