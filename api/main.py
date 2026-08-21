from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import settings

# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Code Generation API",
    description="AI system with 4 agents that collaborate to generate code",
    version="0.1.0"
)

# Allow requests from frontend (CORS = Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Verify API is running"""
    return {
        "status": "healthy",
        "model": settings.OPENAI_MODEL,
        "debug": settings.DEBUG
    }

# Placeholder for later
@app.get("/")
async def root():
    return {"message": "🚀 Multi-Agent Code Generation System"}

if __name__ == "__main__":
    # Run locally: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)