from pathlib import Path

def load_prompts(prompt_dir: Path) -> list[dict]:
    """Load prompts from a directory."""

    prompt_data = []

    for file in sorted(prompt_dir.glob("*.txt")):
        prompt_data.append({
            "name": file.stem,
            "path": file,
            "text": file.read_text(encoding="utf-8").strip()
        })

    return prompt_data
