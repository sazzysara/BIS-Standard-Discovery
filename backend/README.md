# Backend Setup Instructions

## Overview
The FastAPI backend exposes RESTful API endpoints for the BIS Standard Discovery system.

## Prerequisites
- Python 3.9+
- pip
- GROQ_API_KEY environment variable set

## Installation

1. Install backend dependencies:
```bash
pip install -r requirements.txt
```

2. Install project dependencies:
```bash
cd ..
pip install -r requirements.txt
```

## Running the Backend
3. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from: https://console.groq.com/keys

## Running the Backend

### Development Mode

```bash
python main.py
```

Server will start at `http://localhost:8000`

### Production Mode with Uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

This allows access from other machines on the network.

### With Custom Port

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

## API Endpoints

### Health Check
```
GET /health
```

### Discover Standards
```
POST /api/discover
Content-Type: application/json

{
  "description": "Product description here"
}
```

### Batch Discovery
```
POST /api/batch-discover
Content-Type: application/json

[
  {"description": "Product 1"},
  {"description": "Product 2"}
]
```

### Metadata
```
GET /api/metadata
```

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (React dev server)
- Any origin with `--host 0.0.0.0`

## Troubleshooting

### ModuleNotFoundError: No module named 'src'
Ensure you run `main.py` from the `backend/` directory.

### Connection refused on port 8000
Check if port 8000 is already in use: `netstat -an | findstr 8000`

### GROQ_API_KEY not found
Set environment variable: `set GROQ_API_KEY=your_key_here`

## Monitoring

Check the FastAPI interactive documentation:
```
http://localhost:8000/docs
```

Or Swagger UI:
```
http://localhost:8000/redoc
```
