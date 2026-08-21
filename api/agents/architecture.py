import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from config import settings

class ArchitectureAgent:
    """Designs system architecture based on feature specifications."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
    def design_system(self, feature_spec: str) -> dict:
        """Analyzes feature spec and returns system architecture design."""
        
        prompt = self._build_prompt(feature_spec)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract response text - CORRECT WAY
            assistant_message = response.choices[0].message.content
            
            return {
                "agent_name": "Architecture Agent",
                "role": "Designing system architecture",
                "thinking": "Analyzed feature specification and designed architecture",
                "output": assistant_message,
            }
            
        except Exception as e:
            return {
                "agent_name": "Architecture Agent",
                "role": "Designing system architecture",
                "thinking": f"Error: {str(e)}",
                "output": None,
                "error": str(e)
            }
    
    def _build_prompt(self, feature_spec: str) -> str:
        """Constructs the system prompt for the Architecture Agent."""
        return f"""You are an expert system architect. Design production-ready system architecture.

Feature Specification:
{feature_spec}

Provide:

1. **System Overview**: High-level description
2. **API Endpoints**: List REST endpoints (method, path, description)
3. **Database Schema**: Tables, relationships, SQL DDL
4. **Authentication**: JWT, OAuth, sessions, etc
5. **Key Components**: Major system components
6. **Tech Stack**: Technologies (Python + FastAPI recommended)
7. **Potential Challenges**: Scalability, security concerns
8. **Deployment**: Docker, cloud strategy

Be specific and production-ready."""


if __name__ == "__main__":
    agent = ArchitectureAgent()
    spec = "Build a REST API for a todo app with user authentication"
    
    print("Feature Spec:", spec)
    print("\n" + "="*60)
    print("ARCHITECTURE AGENT WORKING...")
    print("="*60 + "\n")
    
    result = agent.design_system(spec)
    
    print(f"Agent: {result['agent_name']}")
    print(f"Role: {result['role']}")
    print(f"Thinking: {result['thinking']}")
    print("\n" + "-"*60)
    print("OUTPUT:")
    print("-"*60)
    if result['output']:
        print(result['output'])
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")