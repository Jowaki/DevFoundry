from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from config import settings
from models import CodeGenerationRequest
from agents.orchestrator import OrchestratorAgent
from agents.pdf_generator import PDFGenerator
import json
import tempfile
import os

app = FastAPI(
    title="Multi-Agent Code Generation API",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
orchestrator = OrchestratorAgent()
pdf_gen = PDFGenerator()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": settings.OPENAI_MODEL,
        "version": "0.2.0"
    }

# Full pipeline with orchestration
@app.post("/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """Full pipeline via orchestrator."""
    try:
        result = orchestrator.orchestrate_generation(request.feature_spec)
        
        if result.get('error'):
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Regenerate with fixes
@app.post("/regenerate-with-fixes")
async def regenerate_with_fixes(data: dict):
    """Regenerate code with fixes for identified issues."""
    try:
        feature_spec = data.get('feature_spec')
        previous_code = data.get('previous_code')
        issues = data.get('issues', {})
        
        if not all([feature_spec, previous_code, issues]):
            raise ValueError("Missing required fields")
        
        result = orchestrator.regenerate_with_fixes(
            feature_spec, 
            previous_code, 
            issues
        )
        
        if result.get('error'):
            raise HTTPException(status_code=500, detail=result['error'])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generate PDF report
@app.post("/generate-pdf")
async def generate_pdf(data: dict):
    """Generate PDF report from pipeline result."""
    try:
        orchestrator_result = data.get('result')
        
        if not orchestrator_result:
            raise ValueError("No result provided")
        
        # Generate PDF
        pdf_bytes = pdf_gen.generate_report(orchestrator_result)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
        
        # Return file
        return FileResponse(
            tmp_path,
            media_type="application/pdf",
            filename="code-generation-report.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": " Multi-Agent Code Generation System v0.2.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)