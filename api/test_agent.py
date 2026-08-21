import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import json
from urllib.request import Request, urlopen

# Test the endpoint
url = "http://localhost:8000/design-architecture"
payload = {
    "feature_spec": "Build a REST API for a todo app with user authentication"
}

print("🔄 Testing /design-architecture endpoint...")
print(f"URL: {url}")
print(f"Payload: {payload}\n")

try:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(f"Status Code: {response.status}\n")
    print("Response:")
    print(json.dumps(json.loads(response_body), indent=2))
except Exception as e:
    print(f"Error: {e}")