# Bot Chat Frontend

A React.js + TypeScript frontend for 1:1 chat bot application, built with Vite following modern best practices.

## Features

- **MessageList**: Displays chat messages in a scrollable list
- **Compose**: Input field for typing messages
- **SendButton**: Button to send messages

## Tech Stack

- React 18.2
- TypeScript 5.x
- Vite 7.x (build tool)
- Axios (HTTP client)

## Project Structure

Following the guide from [sankeyangshu.top](https://sankeyangshu.top/posts/react-init.html):

```
bot-chat-frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Chat.tsx         # Main chat container
│   │   ├── MessageList.tsx  # Message list component
│   │   ├── Message.tsx      # Individual message bubble
│   │   ├── Compose.tsx      # Input field component
│   │   └── SendButton.tsx   # Send button component
│   ├── services/            # API service layer
│   │   └── api.ts
│   ├── types/                # TypeScript type definitions
│   │   └── index.ts
│   ├── styles/               # Global styles (reserved)
│   ├── utils/                # Utility functions (reserved)
│   ├── App.tsx               # Root component
│   └── main.tsx              # Entry point
├── public/                   # Static assets
├── package.json
├── tsconfig.json             # TypeScript configuration
├── tsconfig.app.json         # App-specific TS config
├── vite.config.ts            # Vite configuration with path aliases
└── start-chat-client.sh       # Startup script
```

## Setup

### Prerequisites

- Node.js 20.19+ (or 22.12+)
- npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file (optional):
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

If not set, defaults to `http://localhost:5000/api`

## Development

### Quick Start (Recommended)

Use the startup script:

```bash
./start-chat-client.sh
```

This script will:
- Install dependencies if needed
- Create a `.env` file if it doesn't exist
- Start the development server on `http://localhost:3000`

### Manual Start

Alternatively, run the development server manually:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Build

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

## Path Aliases

The project uses path aliases for cleaner imports:

- `@/*` → `src/*`

Example:
```typescript
import Chat from '@/components/Chat'
import { Message } from '@/types'
import { sendMessage } from '@/services/api'
```

## Components

### MessageList
Displays all messages in the chat. Shows empty state when no messages.

### Compose
Text input field for typing messages. Supports Enter key to send.

### SendButton
Button to send messages. Disabled when input is empty or chat is loading.

## API Integration

The frontend expects a backend API at `http://localhost:5000/api` with the following endpoints:

- `POST /api/chat/session` - Create new session
- `POST /api/chat` - Send message
- `GET /api/health` - Health check

See `src/services/api.ts` for API implementation details.

## TypeScript

All components are fully typed with TypeScript. Type definitions are in `src/types/index.ts`.

## Styling

- Component-specific CSS files
- Global styles in `App.css` and `index.css`
- Responsive design for mobile devices

## References

This project follows the guide from:
- [从零开始搭建一套规范的 Vite + React + TypeScript 前端工程化项目环境](https://sankeyangshu.top/posts/react-init.html)
