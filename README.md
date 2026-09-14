# LLM UML Generator

This project benchmarks multiple LLMs on generating UML class diagrams from natural-language task descriptions. It loads prompts from a local folder, sends them to configured models, extracts PlantUML code from the response, and stores the generated artifacts for comparison.

The project is designed for experiment-driven evaluation and supports OpenAI, Gemini, DeepSeek and Anthropic clients out of the box.

## Features

- Config-driven benchmark runs via `config/test_config.yaml`
- Support for multiple model providers:
  - GPT via OpenAI
  - Gemini via Google GenAI
  - DeepSeek via OpenAI-compatible API
  - Claude via Anthropic
- Prompt filtering and model filtering from the CLI
- Automatic save of raw responses, metadata, extracted PlantUML, and rendered PNGs
- Simple extension point for adding more LLM clients or prompt sets

## Project structure

```text
LLM_UML_Generator/
├── config/
│   └── test_config.yaml      # Default benchmark configuration
├── core/
│   ├── file_manager.py       # File and directory utilities
│   ├── plantUML_renderer.py  # PlantUML extraction and image rendering
│   ├── prompt_loader.py      # Prompt file loading
│   └── prompt_runner.py      # Main benchmarking execution logic
├── llm_clients/
│   ├── base_client.py        # Abstract client interface
│   ├── claude3.py            # Anthropic client
│   ├── deepseek.py           # DeepSeek client
│   ├── gemini.py             # Gemini client
│   └── gpt4.py               # OpenAI GPT client
├── prompts/                  # Prompt files (.txt) used during runs
├── test_runs/                # Generated benchmark outputs
├── main.py                   # CLI entry point
├── requirements.txt
├── README.md
└── .env                      # Local API key storage (not committed)
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd LLM_UML_Generator
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add the API keys for the providers you plan to use:

```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
DEEPSEEK_API_KEY=your_deepseek_key
ANTHROPIC_API_KEY=your_anthropic_key
```

The project reads these values automatically with `python-dotenv`.

## PlantUML setup

The renderer tries to generate a PNG image from extracted PlantUML code, so a PlantUML server must be running locally.

Start the server with Docker:

```bash
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
```

Keep it running while executing the benchmark. If the local server is unreachable, the renderer automatically retries against the public server at `www.plantuml.com`. If no valid PlantUML block is found in a model response, the script will skip image generation and only retain the raw text and metadata.

## Configuration

The default benchmark configuration is stored in `config/test_config.yaml`.

Example:

```yaml
models:
  - name: gpt-4o
    temperature: 0.1
    max_tokens: 8000
    repeat: 1
  - name: deepseek-reasoner
    temperature: 0.1
    max_tokens: 8000
    repeat: 1
  - name: claude-opus-4-20250514
    temperature: 0.1
    max_tokens: 8000
    repeat: 1
  - name: gemini-2.5-pro
    temperature: 0.1
    max_tokens: 8000
    repeat: 1
```

The code reads every entry under `models` and calls the matching client based on the model name prefix:

- `gpt*` -> `GPT4Client()`
- `claude*` -> `ClaudeClient()`
- `gemini*` -> `GeminiClient()`
- `deepseek*` -> `DeepSeekClient()`

If no models are configured, the app falls back to a single GPT-4 run with default parameters.

Prompt files are automatically discovered from `prompts/*.txt` and matched by filename stem.

## Usage

Run all configured prompts against all configured models:

```bash
python main.py
```

Run only a specific prompt:

```bash
python main.py --prompt_name AT-01A
```

Run only a specific model:

```bash
python main.py --model gpt-4o
```

Override runtime parameters for a single CLI run:

```bash
python main.py --temperature 0.7 --max_tokens 5000 --repeat 2
```

You can also combine selection flags:

```bash
python main.py --prompt_name SOMO_B4_A2 --model gemini-2.5-pro --repeat 3
```

## Output structure

Each benchmark run is stored under:

```text
test_runs/<prompt_name>/<model_name>/temp_<temperature>/run_<NN>/
```

Inside each run directory, the script saves:

- `<prompt_name>_<hash>_RESPONSE.txt` — raw model output
- `<prompt_name>_<hash>_METADATA.json` — execution metadata such as model, timestamp, token counts and latency
- `<prompt_name>_<hash>_PUML.puml` — extracted PlantUML if present
- `<prompt_name>_<hash>_DIAGRAM.png` — rendered diagram image if PlantUML code could be extracted

The prompt source itself is also stored once per prompt as:

```text
test_runs/<prompt_name>/<prompt_name>_<hash>.txt
```

## Notes

This repository is intended for benchmarking and analysis rather than for production deployment. It is best suited for running reproducible prompt/model evaluations and comparing resulting UML diagrams across different LLMs.
