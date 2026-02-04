import requests
import json

print("🚀 Starting simple API test...")

API_URL = "https://honeypot-api-898d.onrender.com/honeypot"
API_KEY = "GUVI_HCL_2025_EVAL_YGHn9UoBVBrhoru4q2nDYIMiIHacB9QT"

# Simple payload
payload = {
    "conversation_id": "simple_test",
    "conversation_history": [],
    "incoming_message": {
        "sender": "scammer",
        "text": "You won lottery! Send money to 1234567890@ybl"
    },
    "metadata": {}
}

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

print(f"📡 Testing URL: {API_URL}")
print(f"🔑 Using API Key: {API_KEY[:20]}...")

try:
    print("📤 Sending request...")
    response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    
    print(f"📥 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS! API is working!")
        print(f"Scam detected: {result.get('scam_detected', 'N/A')}")
        print(f"Agent reply: {result.get('agent_reply', 'N/A')}")
        print(f"Status: {result.get('status', 'N/A')}")
        
        print("\n📋 Response format check:")
        required = ['scam_detected', 'agent_reply', 'extracted_intelligence', 'engagement_metrics']
        for field in required:
            print(f"  {'✅' if field in result else '❌'} {field}")
            
        print("\n🎯 Ready for hackathon submission!")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Exception: {type(e).__name__}")
    print(f"Error: {e}")