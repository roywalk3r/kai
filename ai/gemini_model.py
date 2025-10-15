"""Gemini AI model integration for Kai."""

import os
from typing import Dict, Optional

def ask_gemini(prompt: str, system_context: str) -> Optional[str]:
    """
    Ask Gemini AI to interpret a user prompt.
    
    Args:
        prompt: User's natural language request
        system_context: System prompt with context and rules
        
    Returns:
        AI response string or None if error
    """
    try:
        from google import genai
        
        # Get API key from environment
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return None
        
        # Initialize client
        client = genai.Client(api_key=api_key)
        
        # Combine system context and user prompt
        full_prompt = f"{system_context}\n\nUser: {prompt}"
        
        # Generate response
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=full_prompt,
        )
        
        return response.text
        
    except ImportError:
        # google-genai not installed
        return None
    except Exception as e:
        # Other errors (API key invalid, network issues, etc.)
        print(f"Gemini error: {e}")
        return None

def is_gemini_available() -> bool:
    """
    Check if Gemini is available and configured.
    
    Returns:
        True if Gemini can be used, False otherwise
    """
    try:
        from google import genai
        api_key = os.environ.get('GEMINI_API_KEY')
        return api_key is not None and len(api_key) > 0
    except ImportError:
        return False
