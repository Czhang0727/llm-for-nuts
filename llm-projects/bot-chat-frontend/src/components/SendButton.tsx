import React from 'react'
import './SendButton.css'

interface SendButtonProps {
  onClick: () => void
  disabled: boolean
}

function SendButton({ onClick, disabled }: SendButtonProps): JSX.Element {
  return (
    <button type="button" className="SendButton" onClick={onClick} disabled={disabled}>
      Send
    </button>
  )
}

export default SendButton

