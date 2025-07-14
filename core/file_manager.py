from pathlib import Path
from datetime import datetime
import hashlib
import json


def get_prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:10]


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def build_run_directory(base_dir: Path, prompt_name: str, model_name: str, temperature: float) -> Path:
    """Create a directory structure for storing test run results.
    The structure is:
    test_runs/<prompt_name>/<model_name>/<temp>/run_<number>/
    """
    ensure_directory(base_dir)
    temp_folder = f"temp_{str(temperature).replace('.', '_')}"
    model_dir = base_dir / prompt_name / model_name / temp_folder
    model_dir.mkdir(parents=True, exist_ok=True)

    # Find next available run number by checking existing run directories
    existing_numbers = []
    for p in model_dir.iterdir():
        if p.is_dir() and p.name.startswith("run_"):
            try:
                existing_numbers.append(int(p.name.split("_")[1]))
            except (IndexError, ValueError):
                continue

    next_run_number = (max(existing_numbers) if existing_numbers else 0) + 1
    run_dir = model_dir / f"run_{next_run_number:02d}"
    run_dir.mkdir()
    return run_dir

def ensure_directory(path: Path) -> None:
     """Ensure that a directory exists, creating it if necessary."""
     if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"[📁] Created directory: {path}")
        
def save_text(file_path: Path, content: str):
    """Save text content to a file."""
    file_path.write_text(content, encoding="utf-8")

def save_json(file_path: Path, data: dict):
    """Save a dictionary as JSON to a file."""
    file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    
def save_plantuml(file_path: Path, plantuml_code: str):
    """Save PlantUML code to a .puml file."""
    code = plantuml_code.strip()
    
    if "@startuml" in code and "@enduml" in code:
        content = code
    else:
        content = f"@startuml\n{code}\n@enduml"
    
    file_path.write_text(content, encoding="utf-8")