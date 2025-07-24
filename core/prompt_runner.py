from pathlib import Path
from dotenv import load_dotenv
from core.prompt_loader import load_prompts
from core.file_manager import (
    get_prompt_hash,
    build_run_directory,
    save_text,
    save_json,
    save_plantuml
)
from core.plantUML_renderer import extract_plantuml_code, create_plantuml_image
from datetime import datetime

# Load API key from .env file
load_dotenv()

# Directory paths
PROMPT_DIR = Path("prompts")
OUTPUT_BASE = Path("test_runs")

def run_prompts(models, prompt_filter=None, model_filter=None, temperature_override=None, max_tokens_override=None, repeat_override=None):
    """Run all prompts against all configured models.

    Parameters
    ----------
    models : list[dict]
        Configuration for each model including name, client instance,
        default temperature, and repeat count.
        default temperature, repeat count and max tokens.
    prompt_filter : str | None
        If provided, only the prompt with this name will be executed.
    model_filter : str | None
        If provided, only the model with this name will be executed.
    temperature_override : float | None
        Override the model's default temperature.
    max_tokens_override : int | None
        Override the model's default max token value.
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
        
        prompt_txt_path = prompt_folder / f"{prompt_name}_{prompt_hash}.txt"
        if not prompt_txt_path.exists():
            save_text(prompt_txt_path, prompt_text)
            
        for model_config in models:
            model_name = model_config["name"]
            
             # Skip models that do not match the model_filter, if a filter is set
            if model_filter and model_name != model_filter:
                continue
            
            client = model_config["client"]
            temperature = temperature_override if temperature_override is not None else model_config["temperature"]
            max_tokens = max_tokens_override if max_tokens_override is not None else model_config.get("max_tokens", 1000)
            repeat = repeat_override if repeat_override is not None else model_config["repeat"]
            
            for i in range(1, repeat + 1):
                print(f"\n🔁 {prompt_name} | {model_name} | temp={temperature} | run={i}")
                
                parameters = {
                    "model": model_name,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
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
                
                # Access the ID directly from the result dictionary (as added in GeminiClient)
                completion_id = result.get("id", "N/A") 
                raw_response_obj = result.get("raw_response") # Get the raw API response object

                model_version = "N/A"
                created_timestamp = "N/A"
                system_fingerprint = "N/A"
                prompt_tokens = 0
                completion_tokens = 0
                total_tokens = 0

                # Logic to extract metadata based on the type of raw_response_obj
                if model_name.startswith("gpt") or model_name.startswith("deepseek"):
                    # GPT specific attributes
                    if raw_response_obj:
                        model_version = getattr(raw_response_obj, "model", "N/A")
                        created_timestamp = datetime.fromtimestamp(getattr(raw_response_obj, "created", 0)).strftime('%Y-%m-%d %H:%M:%S') if getattr(raw_response_obj, "created", 0) else "N/A"
                        system_fingerprint = getattr(raw_response_obj, "system_fingerprint", "N/A")
                        if hasattr(raw_response_obj, "usage") and raw_response_obj.usage:
                            usage = raw_response_obj.usage
                            prompt_tokens = getattr(usage, "prompt_tokens", 0)
                            completion_tokens = getattr(usage, "completion_tokens", 0)
                            total_tokens = getattr(usage, "total_tokens", 0)
                elif model_name.startswith("gemini"):
                    # Gemini specific attributes
                    if raw_response_obj:
                        model_version = getattr(raw_response_obj, "model_version", "N/A")
                        created_timestamp = getattr(raw_response_obj, "createTime", datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
                        system_fingerprint = "N/A" 
                        if hasattr(raw_response_obj, "usage_metadata") and raw_response_obj.usage_metadata:
                            usage_metadata = raw_response_obj.usage_metadata
                            prompt_tokens = getattr(usage_metadata, "prompt_token_count", 0)
                            completion_tokens = getattr(usage_metadata, "candidates_token_count", 0)
                            total_tokens = getattr(usage_metadata, "total_token_count", 0)
                
                # Save response text
                save_text(run_dir / f"{prompt_name}_{prompt_hash}_RESPONSE.txt", result["text"])
                
                # Create .plum file and PlantUML diagram
                uml_code = extract_plantuml_code(result["text"])
                if uml_code:
                    plum_path = run_dir / f"{prompt_name}_{prompt_hash}_PUML.puml"
                    save_plantuml(plum_path, uml_code)
                    image_path = run_dir / f"{prompt_name}_{prompt_hash}_DIAGRAM.png"
                    create_plantuml_image(uml_code, image_path)
                else:
                    print("[⚠️] No PlantUML code found in response from {model_name}, skipping diagram generation.")
                
                # Save metadata json
                save_json(run_dir / f"{prompt_name}_{prompt_hash}_METADATA.json", {
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

