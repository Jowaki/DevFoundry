import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import OpenAI
from config import settings
from agents.architecture import ArchitectureAgent
from agents.code_gen import CodeGenAgent
from agents.testing import TestingAgent
from agents.security import SecurityAgent
import json
from typing import Dict, List

class OrchestratorAgent:
    """
    Orchestrates all 4 agents and manages the code generation pipeline.
    Collects issues and generates comprehensive reports.
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.architecture_agent = ArchitectureAgent()
        self.code_agent = CodeGenAgent()
        self.testing_agent = TestingAgent()
        self.security_agent = SecurityAgent()
        
    def orchestrate_generation(self, feature_spec: str) -> Dict:
        """
        Runs the complete pipeline and collects all outputs.
        
        Returns:
            Complete pipeline result with all agent outputs and issues
        """
        print(f"\n🎭 ORCHESTRATOR: Starting full pipeline")
        print(f"Feature: {feature_spec[:50]}...\n")
        
        result = {
            "feature_spec": feature_spec,
            "pipeline": {},
            "issues": {"critical": [], "medium": [], "low": []},
            "summary": {}
        }
        
        try:
            # Step 1: Architecture
            print("1️⃣ [ORCHESTRATOR] Running Architecture Agent...")
            arch = self.architecture_agent.design_system(feature_spec)
            result["pipeline"]["architecture"] = arch
            
            if arch.get('error'):
                raise Exception(f"Architecture failed: {arch['error']}")
            
            # Step 2: Code Generation
            print("2️⃣ [ORCHESTRATOR] Running Code Generation Agent...")
            code = self.code_agent.generate_code(arch['output'], feature_spec)
            result["pipeline"]["code"] = code
            
            if code.get('error'):
                raise Exception(f"Code generation failed: {code['error']}")
            
            clean_code = code.get('extracted_code') or code.get('output') or ''
            
            # Step 3: Testing
            print("3️⃣ [ORCHESTRATOR] Running Testing Agent...")
            tests = self.testing_agent.generate_tests(clean_code, arch['output'])
            result["pipeline"]["tests"] = tests
            
            # Step 4: Security
            print("4️⃣ [ORCHESTRATOR] Running Security Agent...")
            security = self.security_agent.audit_code(clean_code, arch['output'])
            result["pipeline"]["security"] = security
            
            # Step 5: Extract issues from security audit
            print("5️⃣ [ORCHESTRATOR] Analyzing security issues...")
            issues = self._extract_issues(security.get('output', ''))
            result["issues"] = issues
            
            # Step 6: Create summary
            print("6️⃣ [ORCHESTRATOR] Creating summary...")
            result["summary"] = self._create_summary(result, issues)
            
            print("✅ Pipeline complete!\n")
            return result
            
        except Exception as e:
            print(f"❌ Pipeline error: {str(e)}")
            result["error"] = str(e)
            return result
    
    def regenerate_with_fixes(self, 
                             feature_spec: str, 
                             previous_code: str,
                             issues: Dict) -> Dict:
        """
        Regenerates code with fixes for identified issues.
        
        Args:
            feature_spec: Original feature request
            previous_code: Code that had issues
            issues: Issues to fix (critical/medium)
        """
        print(f"\n🔄 ORCHESTRATOR: Regenerating code with fixes")
        print(f"Issues to fix: {len(issues.get('critical', []))} critical, {len(issues.get('medium', []))} medium\n")
        
        # Get architecture
        arch = self.architecture_agent.design_system(feature_spec)
        
        # Create enhanced prompt with fixes
        fix_prompt = self._create_fix_prompt(
            feature_spec, 
            arch['output'], 
            previous_code, 
            issues
        )
        
        # Regenerate code
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": fix_prompt}]
            )
            
            full_response = response.choices[0].message.content
            from agents.code_gen import CodeGenAgent
            agent = CodeGenAgent()
            extracted = agent._extract_code_blocks(full_response)
            
            print("✅ Code regenerated with fixes\n")
            
            # Re-run security check on fixed code
            security = self.security_agent.audit_code(extracted, arch['output'])
            
            return {
                "regenerated_code": extracted,
                "full_response": full_response,
                "security_audit": security,
                "issues_fixed": issues
            }
            
        except Exception as e:
            print(f"❌ Regeneration error: {str(e)}")
            return {"error": str(e)}
    
    def _extract_issues(self, security_audit: str) -> Dict:
        """Extract issues from security audit report."""
        issues = {"critical": [], "medium": [], "low": []}
        
        lines = security_audit.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if '🔴 Critical' in line or 'CRITICAL' in line:
                current_section = 'critical'
            elif '🟡 Medium' in line or 'MEDIUM' in line:
                current_section = 'medium'
            elif '🟢' in line or 'Best Practice' in line:
                current_section = None
            elif current_section and line.startswith('-'):
                issue_text = line.lstrip('- ').strip()
                if issue_text:
                    issues[current_section].append(issue_text)
        
        return issues
    
    def _create_fix_prompt(self, 
                          feature_spec: str, 
                          architecture: str, 
                          previous_code: str, 
                          issues: Dict) -> str:
        """Creates prompt for code regeneration with fixes."""
        
        critical_issues = '\n'.join([f"- {i}" for i in issues.get('critical', [])])
        medium_issues = '\n'.join([f"- {i}" for i in issues.get('medium', [])])
        
        return f"""You are an expert Python/FastAPI developer fixing code security issues.

Original Feature: {feature_spec}

Architecture:
{architecture[:1000]}

Previous Code (had issues):
{previous_code[:2000]}

🔴 CRITICAL ISSUES TO FIX:
{critical_issues or 'None'}

🟡 MEDIUM ISSUES TO FIX:
{medium_issues or 'None'}

Generate improved code that:
1. Fixes ALL critical and medium issues
2. Maintains the architecture
3. Adds best practices:
   - Input validation
   - Proper error handling
   - Security best practices
   - Logging
   - Type hints
   - Docstrings
4. Keeps all features from original

Format in markdown code blocks:
```python
# Your improved code here
```

IMPORTANT: Address every single issue listed above!"""

    def _create_summary(self, result: Dict, issues: Dict) -> Dict:
        """Create executive summary."""
        return {
            "total_issues": len(issues.get('critical', [])) + len(issues.get('medium', [])),
            "critical_count": len(issues.get('critical', [])),
            "medium_count": len(issues.get('medium', [])),
            "architecture_complete": "architecture" in result["pipeline"],
            "code_generated": "code" in result["pipeline"],
            "tests_generated": "tests" in result["pipeline"],
            "security_audited": "security" in result["pipeline"],
            "pipeline_status": "complete" if all(k in result["pipeline"] 
                                                  for k in ["architecture", "code", "tests", "security"]) else "partial"
        }