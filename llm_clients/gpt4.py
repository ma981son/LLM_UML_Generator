import os
import time
import openai
from dotenv import load_dotenv
from llm_clients.base_client import LLMClient

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class GPT4Client(LLMClient):
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def send_prompt(self, prompt: str, parameters: dict) -> dict:
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=parameters.get("model", "gpt-4"),
                messages=[{"role": "user", "content": prompt}],
                temperature=parameters.get("temperature", 0.7),
                max_tokens=parameters.get("max_tokens", 1000),
                top_p=parameters.get("top_p", 1.0)
            )

            latency = time.time() - start_time

            return {
                "text": response.choices[0].message.content,
                "latency": latency,
                "status": "success",
                "raw_response": response
            }

        except Exception as e:
            return {
                "text": str(e),
                "latency": None,
                "status": "error",
                "raw_response": None
            }