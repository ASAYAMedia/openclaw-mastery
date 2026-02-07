#!/usr/bin/env python3
"""
Quick test: Verify Gemini API key works for image generation
"""

import requests
import base64

API_KEY = "AIzaSyA6wbgAcyQt788XNe_of8YLAojxbgMlj2I"  # Your key

# Try different model names - some don't support image generation
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Create a simple Pinterest pin design: purple gradient background with white text saying 'Build Your Own AI Assistant', modern minimalist style, 2:3 portrait ratio"
        }]
    }],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"]
    }
}

headers = {"Content-Type": "application/json"}

print("🧪 Testing Gemini API...")

try:
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("✅ API key works!")
        data = response.json()
        
        # Check if image was generated
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            has_image = any("inlineData" in p for p in parts)
            
            if has_image:
                print("✅ Image generation is working!")
                
                # Save the test image
                for part in parts:
                    if "inlineData" in part:
                        image_data = base64.b64decode(part["inlineData"]["data"])
                        with open("test_pin.png", "wb") as f:
                            f.write(image_data)
                        print("✅ Test image saved: test_pin.png")
                        break
            else:
                print("⚠️  API works but no image in response")
                print("Response:", json.dumps(data, indent=2)[:500])
        else:
            print("⚠️  No candidates in response")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"❌ Error: {e}")
