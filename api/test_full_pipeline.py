import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import requests
import json
import time

url = "http://localhost:8000/generate-code"
payload = {
    "feature_spec": "Build a REST API for a todo app with user authentication and database persistence"
}

print("🚀 Testing full pipeline: Architecture → Code")
print(f"URL: {url}")
print(f"Spec: {payload['feature_spec']}\n")

start = time.time()

try:
    response = requests.post(url, json=payload, timeout=120)
    elapsed = time.time() - start
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"⏱️ Time: {elapsed:.2f}s\n")
    
    data = response.json()
    
    print("="*80)
    print("🏗️ ARCHITECTURE AGENT OUTPUT:")
    print("="*80)
    if data.get('architecture'):
        arch = data['architecture']
        print(f"Agent: {arch.get('agent_name')}")
        print(f"Role: {arch.get('role')}")
        print(f"Thinking: {arch.get('thinking')}")
        print(f"\n📋 Architecture Design:\n{arch.get('output', '')[:1000]}...\n")
    
    print("\n" + "="*80)
    print("💻 CODE GENERATION AGENT OUTPUT:")
    print("="*80)
    if data.get('code'):
        code = data['code']
        print(f"Agent: {code.get('agent_name')}")
        print(f"Role: {code.get('role')}")
        print(f"Thinking: {code.get('thinking')}")
        
        extracted = code.get('extracted_code', '')
        if extracted:
            print(f"\n✅ EXTRACTED CODE ({len(extracted)} chars):\n")
            print(extracted[:1500])  # First 1500 chars
            if len(extracted) > 1500:
                print(f"\n... ({len(extracted) - 1500} more characters)")
        else:
            print("\n⚠️ No code extracted")
            print(f"Full response preview: {code.get('output', '')[:500]}...")
        
except Exception as e:
    print(f"❌ Error: {e}")