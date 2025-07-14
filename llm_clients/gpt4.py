import os
import time
import openai
from dotenv import load_dotenv
from llm_clients.base_client import LLMClient

# Load API key from .env file
load_dotenv()

class GPT4Client(LLMClient):
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
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
