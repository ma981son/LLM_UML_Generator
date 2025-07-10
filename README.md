# LLM_UML_Generator

**LLM_UML_Generator** is a Python-based framework for testing and comparing Large Language Models (LLMs) in their ability to generate UML class diagrams from natural language requirements.

This tool is developed as part of a Bachelor's thesis to systematically evaluate LLMs like GPT-4, Claude 3, Google Gemini, and DeepSeek.

---

## Features

- Prompt-based UML class diagram generation using various LLMs
- Modular architecture with unified API access for GPT-4, Claude, Gemini, etc.
- Fully automated test runs with structured output per prompt and model
- Visual UML diagram generation using PlantUML (SVG, PNG)
- Reproducible testing via configuration files and CLI
- Organized storage of all responses, diagrams, and metadata

---

## Project Structure
LLM_UML_Generator/
├── llm_clients/ # API clients for OpenAI, Claude etc.
├── core/ # Test logic and utilities
├── prompts/ # Prompt input files
├── test_runs/ # Auto-generated test results
├── config/ # YAML configuration files
├── cli.py # CLI entry point for running tests
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/ma981son/LLM_UML_Generator.git
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate   # On Windows: .venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Add your API keys to a `.env` file:
    ```env
    OPENAI_API_KEY=your_key_here
    ```

---

## Example CLI Command

CLI Usage
Use main.py to run prompt tests with flexible options:

### Run all prompts with all models
```bash
python main.py
```

### Run a specific prompt by ID
```bash
python main.py --prompt_id "enter_prompt_id"
```

### Run only a specific model
```bash
python main.py --model gpt-4o
```

### Set temperature manually
```bash
python main.py --temperature 0.7
```

### Repeat same test multiple times
```bash
python main.py --repeat 5
```

### Combine all filters
```bash
python main.py --prompt_id "enter_prompt_id" --model gpt-4o --temperature 0.5 --repeat 3
```

