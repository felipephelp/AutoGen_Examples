# Examples Guide

## Execution model

- Each script is a standalone learning unit.
- Scripts use `ReplayChatCompletionClient` for deterministic local outputs.
- No external model API key is required for these didactic runs.

## Recommended order

1. `01_basic_agent_chat.py`
2. `02_tools_file_explorer.py`
3. `03_tools_text_analyzer.py`
4. `04_multi_agent_handoff.py`
5. `05_planner_executor.py`
6. `06_reflection_loop.py`
7. `07_document_explorer.py`
8. `08_batch_explorer.py`
9. `09_human_in_the_loop.py`
10. `10_conversational_coding_assistant.py`

## Example 10 usage

- Scripted deterministic mode (used in batch automation):
  - `python .\examples\10_conversational_coding_assistant.py --mode scripted --backend replay`
- Interactive local demo mode (replay responses):
  - `python .\examples\10_conversational_coding_assistant.py --mode interactive --backend replay`
- Interactive live API mode (OpenAI/Groq compatible):
  - `python .\examples\10_conversational_coding_assistant.py --mode interactive --backend api --model gpt-4o-mini`
- Interactive vLLM mode (OpenAI-compatible server):
  - `python .\examples\10_conversational_coding_assistant.py --mode interactive --backend vllm --model meta-llama/Llama-3.1-8B-Instruct --vllm-base-url http://localhost:8000/v1`
- Interactive Ollama mode:
  - `python .\examples\10_conversational_coding_assistant.py --mode interactive --backend ollama --model llama3.1 --ollama-host http://localhost:11434`
- Local GPU controls:
  - `--gpu-devices 0` sets `CUDA_VISIBLE_DEVICES=0`
  - `--num-gpu 1` sets Ollama GPU usage

Interactive commands:

- `/help`: show usage hints.
- `/reset`: clear local session transcript.
- `/exit`: end session and write output artifacts.

## Debug tips

- If an example fails, inspect `outputs/<example_id>/transcript.md` first.
- Then inspect `tool_calls.jsonl` for function call payloads.
- Validate generated files with `run_metadata.json`.
