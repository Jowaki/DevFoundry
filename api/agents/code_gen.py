import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from config import settings
import re

class CodeGenAgent:
    """
    Generate production ready Python FastAPI code base on architecture
    """
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    def generate_code(self, architecture_design: str, feature_spec: str) -> dict:
        """
        Takes architecture design and generates FastAPI code.
        
        Args:
            architecture_design: Output from Architecture Agent
            feature_spec: Original feature request
            
        Returns:
            dict with: thinking, output (code), extracted_code
        """
        prompt = self._build_prompt(architecture_design, feature_spec)
        print(f"🔄 Code Generation Agent starting...")
        print(f"Architecture length: {len(architecture_design)} chars")
        print(f"Feature spec: {feature_spec[:100]}...")
        
        try:
            respons = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000
            )
        
            full_response = respons.choices[0].message.content
        
            extracted_code = self._extract_code_blocks(full_response)
        
            return {
                "agent_name": "Code Generation Agent",
                "role": "Writing production-ready code",
                "thinking": "Analyzed architecture and generated FastAPI code with proper structure, error handling, and best practices",
                "output": full_response,
                "extracted_code": extracted_code,
                }
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "agent_name": "Code Generation Agent",
                "role": "Writing production-ready code",
                "thinking": f"Error generating code: {str(e)}",
                "output": None,
                "extracted_code": None,
                "error": str(e)
            }
    
    def _build_prompt(self, architecture_design: str, feature_spec: str) -> str:
        """
        Constructs prompt for Code Generation Agent.
        """
        return f"""You are an expert Python/FastAPI developer. Generate production-ready code.
            Feature Specification:
            {feature_spec}

            Architecture Design:
            {architecture_design}

            Generate COMPLETE, RUNNABLE FastAPI code that implements this architecture.

            Requirements:
            1. Use FastAPI framework
            2. Include all endpoints specified in the architecture
            3. Add proper error handling and validation
            4. Include type hints (Pydantic models)
            5. Add docstrings to all functions
            6. Include database models (SQLAlchemy) if needed
            7. Add authentication logic (JWT tokens)
            8. Include request/response schemas
            9. Add logging
            10. Follow Python best practices

            Format your code in markdown code blocks:
            ```python
            # Your code here
            ```

            Start with imports, then models, then endpoints, then main setup.
            Make it production-ready!"""
        
    def _extract_code_blocks(self, response_text: str) -> str:
        """
        Extracts Python code from markdown code blocks.
        GPT returns code in ```python ... ``` blocks, we extract it.
        """
        # Pattern to match ```python ... ```
        patterns = [
            r'```python\n(.*?)\n```',      # ```python ... ```
            r'```Python\n(.*?)\n```',      # ```Python ... ```
            r'```\n(.*?)\n```',             # ``` ... ``` (no language specified)
            r'```(?:python|Python)?\s*(.*?)\s*```',  # Most flexible
        ]
        for pattern in patterns:
            matches = re.findall(pattern, response_text, re.DOTALL)
            if matches:
                print(f"✅ Found {len(matches)} code block(s)")
                return '\n\n---\n\n'.join(matches)  # Join multiple blocks
        
        # If no code blocks found, log debug info
        print(f"No code blocks found in response")
        print(f"Response length: {len(response_text)} characters")
        print(f"First 200 chars: {response_text[:200]}")
        
        return ""
        
    def save_code_to_file(self, extracted_code: str, filename: str = "generated_app.py") -> str:
        """Saves generated code to a file."""
        try:
            filepath = f"/tmp/{filename}"
            with open(filepath, 'w') as f:
                f.write(extracted_code)
            return filepath
        except Exception as e:
            return f"Error saving file: {str(e)}"
        
if __name__ == "__main__":
    # Test with mock architecture
    mock_architecture = """## System Overview
A RESTful API for managing todo items with user authentication.

## API Endpoints
- POST /auth/register - Register new user
- POST /auth/login - Authenticate user
- GET /todos - Get all todos
- POST /todos - Create new todo
- PUT /todos/{id} - Update todo
- DELETE /todos/{id} - Delete todo"""

    agent = CodeGenAgent()
    spec = "Build a REST API for a todo app with user authentication"
    
    print("📋 Feature Spec:", spec)
    print("\n" + "="*60)
    print("💻 CODE GENERATION AGENT WORKING...")
    print("="*60 + "\n")
    
    result = agent.generate_code(mock_architecture, spec)
    
    print(f"Agent: {result['agent_name']}")
    print(f"Role: {result['role']}")
    print(f"Thinking: {result['thinking']}")
    print("\n" + "-"*60)
    print("EXTRACTED CODE:")
    print("-"*60)
    if result['extracted_code']:
        print(result['extracted_code'][:500] + "..." if len(result['extracted_code']) > 500 else result['extracted_code'])
    else:
        print("No code extracted")   