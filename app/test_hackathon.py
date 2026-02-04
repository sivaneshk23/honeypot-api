import requests
import json

API_URL = "https://honeypot-api-898d.onrender.com/honeypot"
API_KEY = "GUVI_HCL_2025_EVAL_YGHn9UoBVBrhoru4q2nDYIMiIHacB9QT"

# Test 1: Minimal valid request
test_payload = {
    "conversation_id": "hackathon_test_1",
    "conversation_history": [],
    "incoming_message": {
        "sender": "scammer",
        "text": "You won $5000!"
    },
    "metadata": {}
}

# Test 2: With empty fields
test_payload_2 = {
    "conversation_id": "test_2",
    "conversation_history": [],
    "incoming_message": {
        "sender": "",
        "text": ""
    },
    "metadata": {}
}

# Test 3: With missing fields (should still work)
test_payload_3 = {
    "conversation_id": "test_3",
    "incoming_message": {
        "sender": "test"
        # missing 'text' field
    }
}

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

print("Testing API with hackathon-style requests...")
print("=" * 50)

for i, payload in enumerate([test_payload, test_payload_2, test_payload_3], 1):
    print(f"\nTest {i}:")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("-" * 30)

print("\n✅ All tests completed!")