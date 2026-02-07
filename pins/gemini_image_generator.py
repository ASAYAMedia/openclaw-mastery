#!/usr/bin/env python3
"""
Gemini Nano Banana Image Generator
Uses Gemini API for text-to-image generation
Free tier: 1,500 requests/day
"""

import requests
import base64
import json
from pathlib import Path

class GeminiImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        # gemini-2.0-flash-exp supports image generation
        self.model = "gemini-2.0-flash-exp"
    
    def generate_image(self, prompt, output_path=None, width=1000, height=1500):
        """
        Generate image from text prompt
        
        Args:
            prompt: Text description of image
            output_path: Where to save PNG (optional)
            width, height: Target dimensions (Gemini may vary slightly)
        
        Returns:
            Path to saved image or None if failed
        """
        
        # Enhance prompt for Pinterest-style pins
        enhanced_prompt = f"""Create a Pinterest pin design image.
        {prompt}
        
        Requirements:
        - Aspect ratio: {width}:{height} (portrait)
        - Style: Modern, clean, professional
        - High quality, eye-catching design
        - Suitable for social media marketing
        """
        
        # API endpoint
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        # Request payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": enhanced_prompt
                }]
            }],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"]
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract image from response
            candidates = data.get("candidates", [])
            if not candidates:
                print("No candidates in response")
                return None
            
            parts = candidates[0].get("content", {}).get("parts", [])
            
            for part in parts:
                if "inlineData" in part:
                    # Extract base64 image
                    image_data = base64.b64decode(part["inlineData"]["data"])
                    
                    # Save to file
                    if output_path is None:
                        output_path = f"generated_pin_{hash(prompt) % 10000}.png"
                    
                    Path(output_path).write_bytes(image_data)
                    print(f"✅ Image saved: {output_path}")
                    return output_path
            
            print("No image found in response")
            return None
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def generate_pinterest_pin(self, title, subtitle, theme="purple-gradient"):
        """
        Generate a complete Pinterest pin
        
        Args:
            title: Main headline text
            subtitle: Supporting text
            theme: Color theme (purple-gradient, blue-gradient, modern, etc.)
        """
        prompt = f"""
        Pinterest pin design (1000x1500 pixels, 2:3 ratio):
        
        Main Title: "{title}"
        Subtitle: "{subtitle}"
        
        Design specifications:
        - {theme} color scheme
        - Bold, readable typography
        - Clean modern layout
        - Call-to-action button area at bottom
        - Professional marketing aesthetic
        - High contrast for readability
        - Suitable for tech/AI tutorial content
        """
        
        filename = f"pin_{title.lower().replace(' ', '_')[:30]}.png"
        return self.generate_image(prompt, filename)


# Example usage for Pinterest pins
if __name__ == "__main__":
    # Initialize with your API key
    API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual key
    
    generator = GeminiImageGenerator(API_KEY)
    
    # Generate pins for your affiliate content
    pins_to_create = [
        {
            "title": "Build Your Own AI Assistant",
            "subtitle": "6 Free Tutorials • Voice • Memory • Automation",
            "theme": "purple gradient with tech aesthetic"
        },
        {
            "title": "23 Free Tools for AI Development", 
            "subtitle": "FFmpeg • Docker • GitHub CLI & More",
            "theme": "dark modern with tool icons"
        },
        {
            "title": "Save 70% on Shipping",
            "subtitle": "Easyship • 250+ Couriers • Global Fulfillment",
            "theme": "green success gradient"
        }
    ]
    
    for pin in pins_to_create:
        print(f"\n🎨 Generating: {pin['title']}")
        result = generator.generate_pinterest_pin(
            pin["title"],
            pin["subtitle"],
            pin["theme"]
        )
        if result:
            print(f"✅ Success: {result}")
        else:
            print("❌ Failed")
