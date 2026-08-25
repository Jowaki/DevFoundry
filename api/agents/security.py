import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from config import settings

class SecurityAgent:
    """
    Audits generated code for security vulnerabilities and best practices.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
    def audit_code(self, generated_code: str, architecture_design: str) -> dict:
        """
        Security audit of generated code.
        
        Args:
            generated_code: Python code to audit
            architecture_design: System architecture context
            
        Returns:
            dict with: thinking, output (audit report)
        """
        
        prompt = self._build_prompt(generated_code, architecture_design)
        
        print(f"🔒 Security Agent starting...")
        print(f"Code to audit: {len(generated_code)} chars")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=3000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            audit_report = response.choices[0].message.content
            print(f"✅ Security audit complete ({len(audit_report)} chars)")
            
            return {
                "agent_name": "🔒 Security Agent",
                "role": "Auditing code for vulnerabilities",
                "thinking": "Analyzed code for OWASP Top 10 vulnerabilities, authentication, authorization, data protection, and best practices",
                "output": audit_report,
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "agent_name": "🔒 Security Agent",
                "role": "Auditing code for vulnerabilities",
                "thinking": f"Error during audit: {str(e)}",
                "output": None,
                "error": str(e)
            }
    
    def _build_prompt(self, generated_code: str, architecture_design: str) -> str:
        """Constructs security audit prompt."""
        return f"""You are an expert security auditor. Audit this code for vulnerabilities.

Generated Code:
{generated_code[:2000]}...

Architecture:
{architecture_design[:1000]}...

Perform a comprehensive security audit checking for:

1. **Authentication & Authorization**
   - Is auth implemented securely?
   - Are permissions properly checked?
   - Is JWT handling correct?

2. **OWASP Top 10**
   - SQL Injection vulnerabilities
   - Cross-site Scripting (XSS)
   - Broken authentication
   - Sensitive data exposure
   - XML External Entities (XXE)
   - Broken access control
   - Security misconfiguration
   - Insecure deserialization
   - Using components with known vulnerabilities
   - Insufficient logging & monitoring

3. **Cryptography & Secrets**
   - Are secrets hardcoded?
   - Is password hashing used?
   - Is HTTPS enforced?
   - Are API keys exposed?

4. **Input Validation**
   - Is all input validated?
   - Are type hints used?
   - Is error handling proper?

5. **Database Security**
   - Are queries parameterized?
   - Is sensitive data encrypted?
   - Are backups secure?

6. **API Security**
   - Is rate limiting present?
   - Is CORS configured securely?
   - Are endpoints authenticated?

Format your report as:

## Security Audit Report

### 🔴 Critical Issues
- Issue 1: Description and fix

### 🟡 Medium Issues
- Issue 1: Description and fix

### 🟢 Best Practices
- Recommendation 1
- Recommendation 2

### ✅ Security Score
X/10 - Summary assessment"""

    def get_severity_score(self, audit_report: str) -> int:
        """Parse security score from report."""
        import re
        match = re.search(r'(\d+)/10', audit_report)
        if match:
            return int(match.group(1))
        return 5  # Default middle score


if __name__ == "__main__":
    mock_code = """from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

# BAD: Password stored in plain text!
users = {}

@app.post("/login")
async def login(user: User):
    # BAD: SQL injection vulnerable!
    query = f"SELECT * FROM users WHERE username = '{user.username}'"
    # ... rest of code"""

    agent = SecurityAgent()
    
    print("🔒 Security Agent Test")
    print("="*60)
    
    result = agent.audit_code(mock_code, "User Auth API")
    
    print(f"\nAgent: {result['agent_name']}")
    print(f"Role: {result['role']}")
    print(f"\n📋 Security Audit:\n{result['output'][:1000]}")