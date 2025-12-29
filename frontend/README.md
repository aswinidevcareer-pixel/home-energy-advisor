# Home Energy Advisor - Frontend

A simple and intuitive Vue.js + TypeScript frontend for the Home Energy Advisor application.

## Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type safety and better developer experience
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client for API calls

## Setup

### Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at http://localhost:5173

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## API Integration

The frontend communicates with the backend through a proxy configured in Vite:

```typescript
// vite.config.ts
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```
