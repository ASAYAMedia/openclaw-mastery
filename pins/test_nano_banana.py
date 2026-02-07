#!/usr/bin/env python3
"""
Test Nano Banana image generation
"""

import requests
import base64

API_KEY = "AIzaSyA6wbgAcyQt788XNe_of8YLAojxbgMlj2I"

# Use the correct model for image generation
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}"

payload = {
    "contents": [{
        "parts": [{
            "text": "Create a Pinterest pin design: purple gradient background, bold white text 'Build Your Own AI Assistant', modern minimalist tech style, 2:3 portrait ratio, professional marketing graphic"
        }]
    }],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"]
    }
}

headers = {"Content-Type": "application/json"}

print("Testing Nano Banana image generation...")

try:
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("API key works!")
        data = response.json()
        
        # Check for image
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            
            for part in parts:
                if "inlineData" in part:
                    # Save image
                    image_data = base64.b64decode(part["inlineData"]["data"])
                    with open("test_pin_nano_banana.png", "wb") as f:
                        f.write(image_data)
                    print("SUCCESS! Image saved: test_pin_nano_banana.png")
                    break
                elif "text" in part:
                    print(f"Text response: {part['text'][:200]}")
        else:
            print("No candidates in response")
            print(f"Full response: {data}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text[:1000])
        
except Exception as e:
    print(f"Error: {e}")
