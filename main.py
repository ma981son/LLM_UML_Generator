# main.py

import argparse
from pathlib import Path
import yaml
from core.prompt_runner import run_prompts
from llm_clients.gpt4 import GPT4Client
from llm_clients.gemini import GeminiClient

# Default config path
CONFIG_PATH = Path("config/test_config.yaml")
    
def get_client(model_name):
    if model_name.startswith("gpt"):
        return GPT4Client()
    #elif model_name.startswith("claude"):
        return ClaudeClient()
    elif model_name.startswith("gemini"):
         return GeminiClient()
    else:
        raise ValueError(f"No client implemented for model: {model_name}")
    
def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    return {}
    
def parse_args():
    parser = argparse.ArgumentParser(description="Run LLM prompt tests.")
    parser.add_argument("--prompt_name", type=str, help="Prompt name to test (e.g. SOMO_B4_A2)")
    parser.add_argument("--model", type=str, help="LLM model name (e.g. gpt-4o)")
    parser.add_argument("--temperature", type=float, help="Sampling temperature")
    parser.add_argument("--max_tokens", type=int, help="Override max tokens")
    parser.add_argument("--repeat", type=int, help="How often to run each test")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_args()
    config = load_config()

    # Build the list of models from config
    model_configs = []
    for model_cfg in config.get("models", []):
        model_name = model_cfg["name"]
        model_cfg["client"] = get_client(model_name)
        model_configs.append(model_cfg)

    # If no models defined in config, fallback to GPT4 with default settings
    if not model_configs:
        model_configs = [{
            "name": "gpt-4o",
            "client": GPT4Client(),
            "temperature": 0.3,
            "max_tokens": 2000,
            "repeat": 1
        }]

    run_prompts(
        models=model_configs,
        prompt_filter=args.prompt_name or config.get("prompt_name"),
        model_filter=args.model,
        temperature_override=args.temperature,
        max_tokens_override=args.max_tokens,
        repeat_override=args.repeat
    )
