from pathlib import Path
from datetime import datetime
import hashlib
import json


def get_prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:10]


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def build_run_directory(base_dir: Path, prompt_name: str, model_name: str, temperature: float) -> Path:
    temp_folder = f"temp_{str(temperature).replace('.', '_')}"
    model_dir = base_dir / prompt_name / model_name / temp_folder
    model_dir.mkdir(parents=True, exist_ok=True)

    # Find next available run number
    existing_runs = [p for p in model_dir.iterdir() if p.name.startswith("run_")]
    next_run_number = len(existing_runs) + 1
    run_dir = model_dir / f"run_{next_run_number:02d}"
    run_dir.mkdir()
    return run_dir

def ensure_directory(path: Path) -> None:
     if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"[📁] Created directory: {path}")
        
def save_text(file_path: Path, content: str):
    file_path.write_text(content, encoding="utf-8")

def save_json(file_path: Path, data: dict):
    file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
