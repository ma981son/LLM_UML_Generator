import os
import time
from anthropic import Anthropic, AsyncAnthropic
from llm_clients.base_client import LLMClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeClient(LLMClient):

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in the .env file.")
        self.client = Anthropic(api_key=api_key)

    def send_prompt(self, prompt: str, parameters: dict) -> dict:
            start_time = time.time()

            try:
                response = self.client.messages.create(
                    model=parameters["model"],
                    max_tokens=parameters.get("max_tokens", 1000),
                    temperature=parameters.get("temperature", 0.3),
                    messages=[{"role": "user", "content": prompt}]
                )

                duration = time.time() - start_time

                return {
                    "text": response.content[0].text, # type: ignore
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
