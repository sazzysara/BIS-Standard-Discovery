# BIS Standard Discovery - React Frontend

Modern React.js frontend for the BIS Standard Discovery system.

## Quick Start

### Prerequisites
- Node.js 14+ and npm
- FastAPI backend running on `http://localhost:8000`

### Installation

```bash
npm install
```

### Development

```bash
npm start
```

The app will open at `http://localhost:3000`

### Environment Configuration

By default, the app connects to `http://localhost:8000` (local FastAPI backend).

For production or custom backend URLs, create a `.env` file in the `frontend/` directory:

```bash
# .env (for production backend)
REACT_APP_API_URL=https://bis-backend-xxxxx.onrender.com
```

See `.env.example` for reference.

Then rebuild and deploy:
```bash
npm run build
```

### Build for Production

```bash
npm build
```

## Features

- 🎨 Modern UI with gradient design
- ⚡ Real-time API integration with FastAPI backend
- 📱 Fully responsive design (mobile, tablet, desktop)
- 🔄 Loading states and error handling
- 📊 Latency display and metadata
- 🎯 Source indication (Fallback vs Retriever+LLM)

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000/api/discover`

### Request
```json
{
  "description": "High-strength concrete beams for bridge construction..."
}
```

### Response
```json
{
  "recommendations": [
    {
      "standard_id": "IS 269:1989",
      "rationale": "..."
    }
  ],
  "latency_seconds": 1.234,
  "matched_by": "Fallback (Deterministic)"
}
```

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── DiscoverForm.js
│   │   ├── DiscoverForm.css
│   │   ├── ResultsDisplay.js
│   │   ├── ResultsDisplay.css
│   │   ├── StandardCard.js
│   │   ├── StandardCard.css
│   │   ├── LoadingSpinner.js
│   │   └── LoadingSpinner.css
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── .gitignore
```

## Deployment

### Local Network Access

1. Start FastAPI backend with `--host 0.0.0.0`
2. Build React: `npm run build`
3. Deploy build folder to a web server
4. Update API URL in code to use server IP: `http://<server-ip>:8000`

## License

Part of the BIS Standard Discovery project.
