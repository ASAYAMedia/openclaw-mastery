#!/usr/bin/env python3
"""
List available Gemini models and test API key
"""

import requests

API_KEY = "AIzaSyA6wbgAcyQt788XNe_of8YLAojxbgMlj2I"

# List available models
print("Fetching available models...")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("\nAvailable models:")
        for model in data.get("models", []):
            name = model.get('name', 'unknown')
            display = model.get('displayName', 'N/A')
            methods = model.get('supportedGenerationMethods', [])
            print(f"  - {name}")
            print(f"    Display: {display}")
            print(f"    Methods: {', '.join(methods) if methods else 'None'}")
            print()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
