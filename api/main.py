from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import settings
from models import CodeGenerationRequest, AgentMessage
from agents.architecture import ArchitectureAgent

# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Code Generation API",
    description="AI system with 4 agents that collaborate to generate code",
    version="0.1.0"
)

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
architecture_agent = ArchitectureAgent()

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": settings.OPENAI_MODEL,
        "debug": settings.DEBUG
    }

# NEW: Design architecture endpoint
@app.post("/design-architecture")
async def design_architecture(request: CodeGenerationRequest):
    """
    Takes a feature spec and returns system architecture design
    """
    try:
        result = architecture_agent.design_system(request.feature_spec)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "🚀 Multi-Agent Code Generation System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)