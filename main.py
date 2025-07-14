# main.py

import argparse
from core.promt_runner import run_prompts
from llm_clients.gpt4 import GPT4Client

# Settings
models = [
    {
        "name": "gpt-4o",
        "client": GPT4Client(),
        "temperature": 0.1,
        "max_tokens": 2000,
        "repeat": 3
    }
]

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

    run_prompts(
        models=models,
        prompt_filter=args.prompt_name,
        model_filter=args.model,
        temperature_override=args.temperature,
        max_tokens_override=args.max_tokens,
        repeat_override=args.repeat,
)
