# llm_clients/deepseek_client.py

import os
from openai import OpenAI
import time
from llm_clients.base_client import LLMClient
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

class DeepSeekClient(LLMClient):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
        )
        if not self.client:
            raise ValueError("DEESEEK_API_KEY is not set in the .env file.") 
    
    def send_prompt(self, prompt: str, parameters: dict) -> dict:
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=parameters["model"],
                messages=[{"role": "user", "content": prompt}],
                temperature=parameters.get("temperature", 0.3),
                max_tokens=parameters.get("max_tokens", 1000)
            )

            duration = time.time() - start_time

            return {
                "text": response.choices[0].message.content,
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
