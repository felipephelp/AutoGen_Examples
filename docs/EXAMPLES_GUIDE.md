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

## Debug tips

- If an example fails, inspect `outputs/<example_id>/transcript.md` first.
- Then inspect `tool_calls.jsonl` for function call payloads.
- Validate generated files with `run_metadata.json`.
