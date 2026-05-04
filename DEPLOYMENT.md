# BIS Standard Discovery - Full Stack Setup

Complete guide to running the React + FastAPI application.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   React Frontend                        │
│            (http://localhost:3000)                      │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/API Calls
                       │
┌──────────────────────▼──────────────────────────────────┐
│                 FastAPI Backend                         │
│             (http://localhost:8000)                     │
├──────────────────────────────────────────────────────────┤
│  ├─ RAG Pipeline (src/rag_pipeline.py)                 │
│  ├─ Chroma Vector Store (data/vectorstore/)            │
│  ├─ Groq LLM Integration                               │
│  └─ Fallback Keyword Matching                          │
└──────────────────────────────────────────────────────────┘
```

## Prerequisites

### System Requirements
- Windows 10/11 or macOS/Linux
- Python 3.9 or higher
- Node.js 14 or higher
- npm 6 or higher

### API Keys
- `GROQ_API_KEY` - Required for LLM functionality

## Quick Start (5 minutes)

### 1. Setup Environment Variables

Create `.env` file in project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Setup Python Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install backend specific dependencies
pip install -r backend/requirements.txt

# Start FastAPI server
cd backend
python main.py
```

Backend will run at: `http://localhost:8000`

### 3. Setup React Frontend

In a new terminal:
```bash
# Navigate to frontend
cd frontend

# Install npm dependencies
npm install

# Start React dev server
npm start
```

Frontend will open at: `http://localhost:3000`

## Detailed Setup

### Backend Setup

1. **Verify Python Environment**
   ```bash
   python --version  # Should be 3.9+
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r backend/requirements.txt
   ```

3. **Set Environment Variables**
   - Windows PowerShell:
     ```powershell
     $env:GROQ_API_KEY = "your_key_here"
     ```
   - Windows CMD:
     ```cmd
     set GROQ_API_KEY=your_key_here
     ```
   - Linux/macOS:
     ```bash
     export GROQ_API_KEY=your_key_here
     ```

4. **Start Backend**
   ```bash
   cd backend
   python main.py
   ```
   
   Or with custom port:
   ```bash
   uvicorn main:app --port 8000 --host 0.0.0.0
   ```

5. **Verify Backend**
   ```
   http://localhost:8000/health
   ```

### Frontend Setup

1. **Verify Node.js Installation**
   ```bash
   node --version  # Should be 14+
   npm --version   # Should be 6+
   ```

2. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Configure API URL**
   - Edit `src/App.js` and update API endpoint if needed
   - Default: `http://localhost:8000/api/discover`

4. **Start Development Server**
   ```bash
   npm start
   ```
   
   Or build for production:
   ```bash
   npm run build
   ```

5. **Access Application**
   ```
   http://localhost:3000
   ```

## Network Access (LAN)

To access from other machines on your network:

### 1. Find Your Machine IP
- Windows:
  ```bash
  ipconfig
  ```
- macOS/Linux:
  ```bash
  ifconfig
  ```
Look for IPv4 Address (e.g., `192.168.1.100`)

### 2. Start Backend with Network Interface
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Update Frontend API URL
Edit `src/App.js`:
```javascript
// Change from:
axios.post('http://localhost:8000/api/discover', ...)

// To:
axios.post('http://192.168.1.100:8000/api/discover', ...)
```

### 4. Build and Serve Frontend
```bash
cd frontend
npm run build

# Serve static files (using http-server or similar)
npx http-server -p 3000 -c-1 build
```

### 5. Access from Other Machine
```
http://192.168.1.100:3000
```

## Troubleshooting

### Backend Issues

**Issue: Port 8000 already in use**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F
```

**Issue: GROQ_API_KEY not found**
- Verify `.env` file exists in project root
- Check environment variable is set: `echo %GROQ_API_KEY%`
- Restart terminal after setting env var

**Issue: ModuleNotFoundError**
- Ensure running from `backend/` directory
- Verify all dependencies installed: `pip list | grep -E "langchain|chromadb|groq"`

### Frontend Issues

**Issue: Cannot find module 'axios'**
```bash
npm install axios
```

**Issue: Port 3000 already in use**
```bash
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
npm start -- --port 3001
```

**Issue: API calls failing**
- Verify backend is running: `http://localhost:8000/health`
- Check browser console for CORS errors
- Verify API endpoint URL in code

## Performance Metrics

Expected metrics with system running:
- **Hit Rate@3**: 100%
- **MRR@5**: 0.95
- **Average Latency**: 1.68s (warm query)
- **Cold-start**: Up to 5s (first query after app start)

## Testing

### Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Discover standards
curl -X POST http://localhost:8000/api/discover \
  -H "Content-Type: application/json" \
  -d '{"description": "High-strength concrete for bridge construction"}'

# View API docs
# Open browser to: http://localhost:8000/docs
```

### Test Frontend
1. Open http://localhost:3000
2. Enter product description
3. Click "Discover Standards"
4. Verify 3 recommendations appear

## Deployment (Production)

### Docker Deployment
```dockerfile
# Build and run in containers
docker-compose up --build
```

### Manual Deployment

**Backend (Linux/Ubuntu Server):**
```bash
# Install dependencies
sudo apt-get install python3 python3-pip
pip3 install -r requirements.txt
pip3 install -r backend/requirements.txt

# Run with systemd or supervisor
# See backend/README.md for details
```

**Frontend (Nginx):**
```bash
cd frontend
npm run build

# Configure Nginx to serve build/ directory
# Setup reverse proxy to http://localhost:8000
```

## Project Structure

```
Rag AI/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt      # Backend dependencies
│   └── README.md            # Backend setup guide
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── README.md            # Frontend setup guide
├── src/
│   ├── rag_pipeline.py      # Core RAG logic
│   └── ingest.py
├── data/
│   └── vectorstore/         # ChromaDB data
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables
├── README.md
└── DEPLOYMENT.md            # This file
```

## Support & Documentation

- **Backend Docs**: `backend/README.md`
- **Frontend Docs**: `frontend/README.md`
- **API Documentation**: `http://localhost:8000/docs`
- **GitHub**: https://github.com/sazzysara/BIS-Standard-Discovery.git

---

**Last Updated**: 2024
**Status**: Production Ready ✓
