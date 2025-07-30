"""OpenRouter API client for the AI village simulation."""
import json
import requests
from typing import Dict, Any, Optional
from config import OPENROUTER_API_KEY, OPENROUTER_API_BASE, DEFAULT_MODEL

class OpenRouterClient:
    """Client for interacting with OpenRouter API."""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        """Initialize the OpenRouter client.
        
        Args:
            api_key: Your OpenRouter API key. Defaults to the one in config.
            base_url: Base URL for the API. Defaults to OpenRouter's API.
        """
        self.api_key = api_key or OPENROUTER_API_KEY
        self.base_url = base_url or OPENROUTER_API_BASE
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/yourusername/ai-village-simulator",  # Optional, for tracking
            "X-Title": "AI Village Simulator"  # Optional, for tracking
        }
    
    def chat_completion(
        self,
        messages: list[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a chat completion using OpenRouter.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            model: Model to use. Defaults to the one in config.
            temperature: Sampling temperature. Defaults to 0.7.
            max_tokens: Maximum number of tokens to generate. Defaults to 1000.
            **kwargs: Additional parameters to pass to the API.
            
        Returns:
            The API response as a dictionary.
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model or DEFAULT_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        response = requests.post(
            url,
            headers={
                **self.headers,
                "Content-Type": "application/json"
            },
            data=json.dumps(payload)
        )
        
        response.raise_for_status()
        return response.json()
    
    def list_models(self) -> Dict[str, Any]:
        """List all available models from OpenRouter.
        
        Returns:
            Dictionary containing the list of available models.
        """
        url = f"{self.base_url}/models"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == "__main__":
    client = OpenRouterClient()
    
    # List available models
    try:
        models = client.list_models()
        print("Available models:")
        for model in models.get('data', [])[:5]:  # Show first 5 models
            print(f"- {model['id']} (context: {model.get('context_length', 'N/A')} tokens)")
    except Exception as e:
        print(f"Error listing models: {e}")
    
    # Example chat completion
    try:
        response = client.chat_completion(
            messages=[
                {"role": "user", "content": "Hello, how are you?"}
            ],
            model=DEFAULT_MODEL
        )
        print("\nChat completion response:")
        print(response.get('choices', [{}])[0].get('message', {}).get('content', 'No response'))
    except Exception as e:
        print(f"Error in chat completion: {e}")
