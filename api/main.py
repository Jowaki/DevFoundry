from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import settings
from models import CodeGenerationRequest, AgentMessage
from agents.architecture import ArchitectureAgent
from agents.code_gen import CodeGenAgent

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
code_gen_agent = CodeGenAgent()

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": settings.OPENAI_MODEL,
        "debug": settings.DEBUG
    }

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

@app.post("/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """
    Full pipeline: Architecture → Code
    """
    try:
        arch_result = architecture_agent.design_system(request.feature_spec)
        
        if arch_result.get("error"):
            raise HTTPException(status_code=500, detail=arch_result["error"])
        
        code_result = code_gen_agent.generate_code(arch_result["output"], request.feature_spec)
        
        if code_result.get("error"):
            raise HTTPException(status_code=500, detail=code_result["error"])
        
        return {
            "feature_spec": request.feature_spec,
            "architecture_design": arch_result, 
            "code_generation": code_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "🚀 Multi-Agent Code Generation System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
@app.post("/test-code-gen")
async def test_code_gen():
    """Simple test endpoint"""
    try:
        from agents.code_gen import CodeGenAgent
        agent = CodeGenAgent()
        result = agent.generate_code(
            "Simple todo API", 
            "Build a todo app"
        )
        return result
    except Exception as e:
        return {"error": str(e)}