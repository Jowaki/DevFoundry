import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from config import settings
import re

class TestingAgent:
    """
    Generate comprehensive pytest testcases based on generated code
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
    def generate_tests(self, generated_code: str, architecture_design: str) -> dict:
        """
        Takes generated code and creates pytest test cases.
        
        Args:
            generated_code: Python code to test
            architecture_design: System architecture for context
            
        Returns:
            dict with: thinking, output (tests), extracted_tests
        """
        
        prompt = self._build_prompt(generated_code, architecture_design)
        
        print(f"Test Generation Agent Starting...")
        print(f"Code to test: {len(generated_code)} chars")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000
            )
            
            full_response = response.choices[0].message.content
            print(f"Got test response ({len(full_response)} chars)")
            
            # Extract the test cases from the response
            extracted_tests = self._extract_test_cases(full_response)
            print(f"Extracted {len(extracted_tests)} chars")
            
            return {
                "agent_name": "TestingAgent",
                "role": "Generate comprehensive pytest testcases based on generated code",
                "thinking":"Analyzed code and generated pytest test cases with good coverage, edge cases, and mocking",
                "output": full_response,
                "extracted_tests": extracted_tests
            }
            
        except Exception as e:
            print(f"Error generating test cases: {e}")
            return {
                "agent_name": "TestingAgent",
                "role": "Generate comprehensive pytest testcases based on generated code",
                "thinking":f"Error occurred during test case generation: {str(e)}",
                "output": None,
                "extracted_tests": None, 
                "error": str(e)
            }
            
    def _build_prompt(self, generated_code: str, architecture_design: str) -> str:
        """
        Constructs prompt for Testing Agent
        """
        return f"""You are an expert pytest developer. Generate comprehensive test cases.

        Generated Code:
        {generated_code[:2000]}...

        Architecture:
        {architecture_design[:1000]}...

        Generate COMPLETE pytest test cases that:

        1. Test all endpoints and functions
        2. Include happy path and edge cases
        3. Test error conditions
        4. Use proper mocking for dependencies
        5. Include fixtures for common setup
        6. Test authentication/authorization if present
        7. Test database operations if present
        8. Achieve >80% code coverage
        9. Use descriptive test names
        10. Include docstrings

        Format code in markdown code blocks:
        ```python
        # Your test code here
        ```

        Include:
        - imports and fixtures
        - test classes or functions
        - parametrized tests for multiple scenarios
        - setup/teardown code
        - mock definitions

        Make tests production-ready!"""
        
    
    def _extract_test_cases(self, response_text: str) -> str:
        """Extract Python test code from markdown blocks"""
        import re 
        patterns = [
            r'```python\n(.*?)\n```',
            r'```Python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```(?:python|Python)?\s*(.*?)\s*```',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response_text, re.DOTALL)
            if matches:
                print(f"✅ Found {len(matches)} test block(s)")
                return '\n\n---\n\n'.join(matches)
        
        print(f"⚠️ No test blocks found")
        return ""


if __name__ == "__main__":
    mock_code = """from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    title: str
    completed: bool = False

todos = []

@app.post("/todos")
async def create_todo(todo: Todo):
    todos.append(todo)
    return todo"""

    agent = TestingAgent()
    
    print("🧪 Testing Agent Test")
    print("="*60)
    
    result = agent.generate_tests(mock_code, "Todo REST API")
    
    print(f"\nAgent: {result['agent_name']}")
    print(f"Role: {result['role']}")
    print(f"\n📋 Generated Tests:\n{result['extracted_tests'][:800]}")
           