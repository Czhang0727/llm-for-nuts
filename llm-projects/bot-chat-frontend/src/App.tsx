import React from 'react'
import Chat from '@/components/Chat'
import './App.css'

function App(): JSX.Element {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Bot Chat</h1>
        <p>1:1 Chat with AI Assistant</p>
      </header>
      <main className="App-main">
        <Chat />
      </main>
    </div>
  )
}

export default App
