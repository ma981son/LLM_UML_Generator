# main.py

import argparse
from core.test_runner import run_all_tests
from llm_clients.gpt4 import GPT4Client

# Settings
models = [
    {
        "name": "gpt-4o",
        "client": GPT4Client(),
        "temperature": 0.3,
        "repeat": 2
    }
]

def parse_args():
    parser = argparse.ArgumentParser(description="Run LLM prompt tests.")
    parser.add_argument("--prompt_id", type=str, help="Prompt ID to test (e.g. SOMO_B4_A2)")
    parser.add_argument("--model", type=str, help="LLM model name (e.g. gpt-4o)")
    parser.add_argument("--temperature", type=float, help="Sampling temperature")
    parser.add_argument("--repeat", type=int, help="How often to run each test")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    run_all_tests(
    models=models,  # ✅ pass models explicitly
    prompt_filter=args.prompt_id,
    model_filter=args.model,
    temperature_override=args.temperature,
    repeat_override=args.repeat
)
