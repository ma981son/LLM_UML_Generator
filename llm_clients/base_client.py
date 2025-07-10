from abc import ABC, abstractmethod

# Base class for LLM clients
# This class defines the interface for sending prompts to different LLMs.
# Each specific LLM client (e.g., OpenAI, Anthropic, etc.) should
# implement this interface to handle the specifics of their API.
# The `send_prompt` method should be implemented to send a prompt to the LLM
# and return the response in a structured format.
class LLMClient(ABC):

    @abstractmethod
    def send_prompt(self, prompt: str, parameters: dict) -> dict:
        pass
