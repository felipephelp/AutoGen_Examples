# Quickstart

1. Create environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pip install -e .
```

2. Run one example:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src)
.\.venv\Scripts\python.exe .\examples\02_tools_file_explorer.py
```

3. Run all examples (prints input and output per example):

```powershell
.\scripts\run_all_examples.ps1
```

Notes:

- `run_all_examples.ps1` suppresses noisy replay warnings and prints only the useful content.
- Individual scripts still print their own summary by default.

4. Inspect generated outputs:

```text
outputs/02_tools_file_explorer/
```

5. Run conversational coding assistant (example 10):

```powershell
# Deterministic scripted run (no API needed)
.\.venv\Scripts\python.exe .\examples\10_conversational_coding_assistant.py --mode scripted --backend replay

# Interactive live run (requires OPENAI_API_KEY or GROQ_API_KEY)
.\.venv\Scripts\python.exe .\examples\10_conversational_coding_assistant.py --mode interactive --backend api --model gpt-4o-mini

# Interactive vLLM run (OpenAI-compatible local server)
.\.venv\Scripts\python.exe .\examples\10_conversational_coding_assistant.py --mode interactive --backend vllm --model meta-llama/Llama-3.1-8B-Instruct --vllm-base-url http://localhost:8000/v1

# Interactive Ollama run with GPU allocation
.\.venv\Scripts\python.exe .\examples\10_conversational_coding_assistant.py --mode interactive --backend ollama --model llama3.1 --gpu-devices 0 --num-gpu 1
```
