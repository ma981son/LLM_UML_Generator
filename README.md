# LLM_UML_Generator

LLM_UML_Generator is a lightweight framework for benchmarking large language models on the task of generating UML class diagrams from natural language descriptions.

The project started as part of a Bachelor's thesis and provides a minimal set of tools for loading prompts, sending them to different LLMs and storing the resulting diagrams and metadata.

## Features

- Modular client interface (currently GPT‑4) for easy extension to other APIs
- Command line interface for running prompts with configurable parameters
- Automatic storage of responses, metadata and PlantUML diagrams
- Simple project layout that can be adapted for custom experiments

## Project layout

```
LLM_UML_Generator/
├── core/         # Test logic and utilities
├── llm_clients/  # API client implementations
├── prompts/      # Input prompt files
├── test_runs/    # Generated results (created at runtime)
├── main.py       # CLI entry point
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/ma981son/LLM_UML_Generator.git
   cd LLM_UML_Generator
   ```
2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Provide your API keys via a `.env` file
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Usage

Run the CLI to execute all prompts with the default model configuration:

```bash
python main.py
```

Useful options:

```bash
python main.py --prompt_name SOMO_B4_A2    # run only a single prompt
python main.py --model gpt-4o              # select a specific model
python main.py --temperature 0.7           # override sampling temperature
python main.py --repeat 3                  # repeat the test multiple times
```

Generated files are placed under `test_runs/<prompt_name>/<model>/<temp>/run_*` including the raw LLM response, metadata and a PlantUML diagram if one could be extracted.

---

This repository contains only a minimal example setup. Extend the prompt collection, add more LLM clients or adjust the testing logic to suit your own evaluation requirements.
