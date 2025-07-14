from pathlib import Path
from dotenv import load_dotenv
from core.prompt_loader import load_prompts
from core.file_manager import (
    get_prompt_hash,
    build_run_directory,
    save_text,
    save_json
)
from core.plantUML_renderer import extract_plantuml_code, create_plantuml_image
from datetime import datetime

# Load API key from .env file
load_dotenv()

# Directory paths
PROMPT_DIR = Path("prompts")
OUTPUT_BASE = Path("test_runs")

def run_prompts(models, prompt_filter=None, model_filter=None, temperature_override=None, repeat_override=None):
    """Run all prompts against all configured models.

    Parameters
    ----------
    models : list[dict]
        Configuration for each model including name, client instance,
        default temperature, and repeat count.
    prompt_filter : str | None
        If provided, only the prompt with this name will be executed.
    model_filter : str | None
        If provided, only the model with this name will be executed.
    temperature_override : float | None
        Override the model's default temperature.
    repeat_override : int | None
        Override how many times each test should be repeated.
    """
    
    prompts = load_prompts(PROMPT_DIR)
    
    # Ensure the prompt directory exists and contains prompts
    for prompt in prompts:
        prompt_name = prompt["name"]
        
        # Skip prompts that do not match the prompt_filter, if a filter is set
        if prompt_filter and prompt_name != prompt_filter:
            continue
        
        prompt_text = prompt["text"]
        prompt_hash = get_prompt_hash(prompt_text)
        prompt_folder = OUTPUT_BASE / prompt_name
        prompt_folder.mkdir(parents=True, exist_ok=True)
        
        prompt_txt_path = prompt_folder / "prompt.txt"
        if not prompt_txt_path.exists():
            save_text(prompt_txt_path, prompt_text)
            
        for model_config in models:
            model_name = model_config["name"]
            
             # Skip models that do not match the model_filter, if a filter is set
            if model_filter and model_name != model_filter:
                continue
            
            client = model_config["client"]
            temperature = temperature_override if temperature_override is not None else model_config["temperature"]
            repeat = repeat_override if repeat_override is not None else model_config["repeat"]
            
            for i in range(1, repeat + 1):
                print(f"\n🔁 {prompt_name} | {model_name} | temp={temperature} | run={i}")
                
                parameters = {
                    "model": model_name,
                    "temperature": temperature,
                    "max_tokens": 1000
                }
                
                # Build the run directory for this prompt,model and temperature
                run_dir = build_run_directory(
                    base_dir=OUTPUT_BASE,
                    prompt_name=prompt_name,
                    model_name=model_name,
                    temperature=temperature,
                )
                
                # Send the prompt to the LLM client
                result = client.send_prompt(prompt_text, parameters)
                
                # Save the raw response and metadata
                raw = result["raw_response"]
                completion_id = raw.id
                model_version = raw.model
                system_fingerprint = getattr(raw, "system_fingerprint", "N/A")
                created_timestamp = datetime.fromtimestamp(raw.created).strftime('%Y-%m-%d %H:%M:%S')
                usage = raw.usage
                prompt_tokens = usage.prompt_tokens
                completion_tokens = usage.completion_tokens
                total_tokens = usage.total_tokens
                
                # Save response text
                save_text(run_dir / f"{prompt_name}_{model_name}_RESPONSE.txt", result["text"])
                
                # Create PlantUML diagram
                uml_code = extract_plantuml_code(result["text"])
                if uml_code:
                    image_path = run_dir / f"{prompt_name}_{model_name}_diagram.png"
                    create_plantuml_image(uml_code, image_path)

                # Save metadata json
                save_json(run_dir / f"{prompt_name}_{model_name}_METADATA.json", {
                    "prompt_name": prompt_name,
                    "model": model_name,
                    "model_version": model_version,
                    "temperature": temperature,
                    "prompt_hash": prompt_hash,
                    "completion_id": completion_id,
                    "system_fingerprint": system_fingerprint,
                    "timestamp": created_timestamp,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                    "latency": result.get("latency"),
                    "status": result.get("status")
                })
                
                print(f"✅ Saved to: {run_dir}")

