import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from llm_clients.base_client import LLMClient

# Load API key from .env file
load_dotenv()

class GeminiClient(LLMClient):
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the .env file.")
        
        self.client = genai.Client(api_key=api_key)
        
    def send_prompt(self, prompt: str, parameters: dict) -> dict:
        start_time = time.time()
        
        generated_text = ""

        try:
            model_name = parameters["model"]
            generation_config = {
                "temperature": parameters.get("temperature", 0.3),
                "max_output_tokens": parameters.get("max_tokens", 1000),
            }
            
            response = self.client.models.generate_content(
                model=model_name,
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
                config=types.GenerateContentConfig(**generation_config)
            )
            
            duration = time.time() - start_time
            
            if response.candidates:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Check if 'text' attribute exists and is not None
                        if hasattr(part, 'text') and part.text is not None:
                            generated_text += part.text
            return {
                "text": generated_text,
                "latency": duration,
                "raw_response": response
            }

        except Exception as e:
            return {
                "text": f"ERROR: {str(e)}",
                "latency": None,
                "status": "error",
                "raw_response": None
            }