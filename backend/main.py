from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import sys
import os
import time
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import BISRAGPipeline
from typing import Optional

app = FastAPI(
    title="BIS Standard Discovery API",
    description="AI-Powered Recommendation System for Indian Building Material Standards",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy pipeline: avoid heavy imports/initialization at module import time
pipeline: Optional[BISRAGPipeline] = None


@app.on_event("startup")
async def create_and_warm_pipeline():
    """Create the pipeline on startup and warm it up to avoid cold-start latency."""
    global pipeline
    print("🚀 FastAPI startup: initializing pipeline...")
    try:
        pipeline = BISRAGPipeline()
        # run warm-up in a thread to avoid blocking the event loop
        await asyncio.to_thread(pipeline.warm_up_retriever)
        print("✓ Pipeline initialized and warmed up")
    except Exception as e:
        # log the error; pipeline will remain None and endpoints should return 503
        pipeline = None
        print(f"⚠ Pipeline initialization failed on startup: {e}")

# Request/Response models
class DiscoverRequest(BaseModel):
    description: str

class StandardRecommendation(BaseModel):
    standard_id: str
    rationale: str

class DiscoverResponse(BaseModel):
    recommendations: list[StandardRecommendation]
    latency_seconds: float
    matched_by: str

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "BIS Discovery API"}

# Main discovery endpoint
@app.post("/api/discover", response_model=DiscoverResponse)
async def discover_standards(request: DiscoverRequest):
    """
    Discover applicable BIS standards for a product description.
    
    Args:
        request: DiscoverRequest with product description
        
    Returns:
        DiscoverResponse with 3 recommended standards and latency info
    """
    if not request.description or len(request.description.strip()) == 0:
        raise HTTPException(status_code=400, detail="Description cannot be empty")
    
    try:
        # Ensure pipeline was initialized successfully
        if pipeline is None:
            raise HTTPException(status_code=503, detail="Service unavailable: pipeline not initialized")

        start_time = time.time()
        recommendations = pipeline.get_recommendations(request.description)
        latency = time.time() - start_time

        # Determine if matched by fallback
        matched_by = "Fallback (Deterministic)" if pipeline.last_fallback else "Retriever + LLM"

        return DiscoverResponse(
            recommendations=[
                StandardRecommendation(**rec) for rec in recommendations
            ],
            latency_seconds=round(latency, 4),
            matched_by=matched_by
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Batch discovery endpoint
@app.post("/api/batch-discover")
async def batch_discover(requests: list[DiscoverRequest]):
    """
    Batch discovery for multiple queries.
    """
    results = []
    for req in requests:
        try:
            result = await discover_standards(req)
            results.append({"query": req.description, "result": result})
        except Exception as e:
            results.append({"query": req.description, "error": str(e)})
    
    return {"results": results}

# Metadata endpoint
@app.get("/api/metadata")
async def metadata():
    """
    Return system metadata and available standards info.
    """
    return {
        "system": "BIS Standard Discovery",
        "version": "1.0.0",
        "common_standards": pipeline.common_standards,
        "fallback_enabled": True,
        "lru_cache_enabled": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
