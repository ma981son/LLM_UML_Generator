import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from plantuml import PlantUML

# Public PlantUML rendering server
plantuml = PlantUML(url="http://www.plantuml.com/plantuml/img/")

def extract_plantuml_code(text: str) -> str:
    """Extract PlantUML code from a text block."""
    match = re.search(r'```plantuml\n(.*?)\n```', text, re.DOTALL)
    return match.group(1).strip() if match else ""

def create_plantuml_image(plantuml_code: str, output_image_path: Path):
    """Create a PlantUML image from the provided code and save it to the specified path."""
    with NamedTemporaryFile("w+", suffix=".puml", delete=False, encoding="utf-8") as tmp_file:
        tmp_file.write(f"@startuml\n{plantuml_code}\n@enduml\n")
        tmp_file_path = Path(tmp_file.name)

    output_image_path.parent.mkdir(parents=True, exist_ok=True)
    plantuml.processes_file(str(tmp_file_path))

    generated_img = tmp_file_path.with_suffix(".png")
    if generated_img.exists():
        generated_img.rename(output_image_path)

    tmp_file_path.unlink(missing_ok=True)
