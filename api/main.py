from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import settings
from models import CodeGenerationRequest
from agents.architecture import ArchitectureAgent
from agents.code_gen import CodeGenAgent
from agents.testing import TestingAgent
from agents.security import SecurityAgent

app = FastAPI(
    title="Multi-Agent Code Generation API",
    description="AI system with 4 agents that collaborate to generate code",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize all agents
architecture_agent = ArchitectureAgent()
code_gen_agent = CodeGenAgent()
testing_agent = TestingAgent()
security_agent = SecurityAgent()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": settings.OPENAI_MODEL,
        "debug": settings.DEBUG
    }

# Full pipeline endpoint
@app.post("/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """
    Full pipeline: Architecture → Code → Tests → Security
    """
    try:
        print(f"\n🚀 Starting full pipeline for: {request.feature_spec[:50]}...")
        
        # Step 1: Architecture
        print("1️⃣ Architecture Agent...")
        arch_result = architecture_agent.design_system(request.feature_spec)
        if arch_result.get('error'):
            raise HTTPException(status_code=500, detail=arch_result['error'])
        
        # Step 2: Code Generation
        print("2️⃣ Code Generation Agent...")
        code_result = code_gen_agent.generate_code(
            arch_result['output'],
            request.feature_spec
        )
        if code_result.get('error'):
            raise HTTPException(status_code=500, detail=code_result['error'])
        
        # Get clean code for next steps
        clean_code = code_result.get('extracted_code') or code_result.get('output') or ''
        
        # Step 3: Testing
        print("3️⃣ Testing Agent...")
        test_result = testing_agent.generate_tests(clean_code, arch_result['output'])
        
        # Step 4: Security
        print("4️⃣ Security Agent...")
        security_result = security_agent.audit_code(clean_code, arch_result['output'])
        
        print("✅ All agents complete!\n")
        
        # Return complete response
        return {
            "feature_spec": request.feature_spec,
            "architecture": arch_result,
            "code": code_result,
            "tests": test_result,
            "security": security_result
        }
        
    except Exception as e:
        print(f"❌ Pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "🚀 Multi-Agent Code Generation System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)