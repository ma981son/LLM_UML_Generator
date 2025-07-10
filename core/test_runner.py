from pathlib import Path
from dotenv import load_dotenv
from core.prompt_loader import load_prompts
from core.file_manager import (
    get_prompt_hash,
    get_timestamp,
    build_run_directory,
    ensure_directory,
    save_text,
    save_json
)
from llm_clients.gpt4 import GPT4Client

# Load API key from .env file
load_dotenv()

# Settings
models = [
    {
        "name": "gpt-4o",
        "client": GPT4Client(),
        "temperature": 0.3,
        "repeat": 1
    }
]

# Directory paths
PROMPT_DIR = Path("prompts")
OUTPUT_BASE = Path("test_runs")

def run_all_tests():
    
    ensure_directory(PROMPT_DIR)
    prompts = load_prompts(PROMPT_DIR)

    for prompt in prompts:
        prompt_id = prompt["id"]
        prompt_text = prompt["text"]
        prompt_hash = get_prompt_hash(prompt_text)

        prompt_folder = OUTPUT_BASE / prompt_id
        ensure_directory(prompt_folder)

        prompt_txt_path = prompt_folder / "prompt.txt"
        if not prompt_txt_path.exists():
            save_text(prompt_txt_path, prompt_text)

        for model_config in models:
            model_name = model_config["name"]
            client = model_config["client"]
            temperature = model_config["temperature"]
            repeat = model_config["repeat"]

            for _ in range(1, repeat + 1):
                print(f"\n🔁 {prompt_id} | {model_name} | temp={temperature}")

                parameters = {
                    "model": model_name,
                    "temperature": temperature,
                    "max_tokens": 1000
                }

                result = client.send_prompt(prompt_text, parameters)

                run_dir = build_run_directory(
                    base_dir=OUTPUT_BASE,
                    prompt_id=prompt_id,
                    model_name=model_name,
                    temperature=temperature,
                )

                # Save results
                save_text(run_dir / "prompt.txt", prompt_text)
                save_text(run_dir / "response.txt", result["text"])
                save_json(run_dir / "metadata.json", {
                    "prompt_id": prompt_id,
                    "model": model_name,
                    "temperature": temperature,
                    "prompt_hash": prompt_hash,
                    "timestamp": get_timestamp(),
                    "latency": result.get("latency"),
                    "status": result.get("status")
                })

                print(f"✅ gespeichert in: {run_dir}")

if __name__ == "__main__":
    run_all_tests()
