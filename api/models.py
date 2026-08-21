from pydantic import BaseModel
from typing import List, Optional

class CodeGenerationRequest(BaseModel):
    """What the user sends to /generate"""
    feature_spec: str  # e.g., "Build a REST API for a todo app"
    language: str = "python"  # Default to Python
    
class AgentMessage(BaseModel):
    """One agent's reasoning output"""
    agent_name: str  # e.g., "Architecture Agent"
    role: str  # e.g., "Designing system architecture"
    thinking: str  # What the agent is thinking
    output: Optional[str] = None  # Final output (code, tests, etc)

class CodeGenerationResponse(BaseModel):
    """Full response after all agents run"""
    id: str
    feature_spec: str
    agent_messages: List[AgentMessage]
    final_code: Optional[str] = None
    final_tests: Optional[str] = None
    security_audit: Optional[str] = None