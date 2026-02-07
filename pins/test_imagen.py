#!/usr/bin/env python3
"""
Test Imagen 4 image generation (different quota than Gemini)
"""

import requests
import base64

API_KEY = "AIzaSyA6wbgAcyQt788XNe_of8YLAojxbgMlj2I"

# Try Imagen 4 - uses different endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"

payload = {
    "instances": [{
        "prompt": "Pinterest pin design with purple gradient background, bold white text saying 'Build Your Own AI Assistant', modern tech minimalist style, portrait 2:3 ratio, professional marketing graphic, clean typography"
    }],
    "parameters": {
        "sampleCount": 1,
        "aspectRatio": "3:4"
    }
}

headers = {"Content-Type": "application/json"}

print("Testing Imagen 4...")

try:
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("SUCCESS!")
        data = response.json()
        
        # Save image
        predictions = data.get("predictions", [])
        if predictions:
            for pred in predictions:
                if "bytesBase64Encoded" in pred:
                    image_data = base64.b64decode(pred["bytesBase64Encoded"])
                    with open("test_pin_imagen.png", "wb") as f:
                        f.write(image_data)
                    print("Image saved: test_pin_imagen.png")
                else:
                    print(f"Prediction: {pred}")
        else:
            print(f"No predictions. Response: {data}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text[:1000])
        
except Exception as e:
    print(f"Error: {e}")
