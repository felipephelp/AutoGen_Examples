# Per-Example Execution Flow (Operational Detail)

This document explains, for each example (`01` to `10`), exactly:
- what runs (function-level sequence),
- which AutoGen primitives are used,
- which tools are called (if any),
- expected input and expected final output,
- extra output artifacts beyond the standard files.

## Standard output artifacts (all examples)

Each example writes these files in `outputs/<example_id>/`:

- `run_metadata.json`
- `input_text.txt`
- `example_output.txt`
- `transcript.md`
- `result.json`
- `tool_calls.jsonl`

Validation path used by every example:
- `_common.assert_standard_outputs(example_id)` ->
- `validators.validate_output_files(...)` ->
- if missing/empty required files: `RuntimeError`.

## AutoGen primitives used in this repository

- `autogen_agentchat.agents.AssistantAgent`
- `autogen_agentchat.teams.RoundRobinGroupChat` (examples 04 and 05)
- `autogen_ext.models.replay.ReplayChatCompletionClient`
- `autogen_core.models.CreateResult` + `autogen_core.FunctionCall` (tool-call simulation)

## Example-by-example flow

### 01_basic_agent_chat

- Runtime sequence:
  1. `build_replay_assistant(...)` creates one `AssistantAgent` with replay response.
  2. `run_agent_example(...)` executes `assistant.run(task=...)`.
  3. `export_task_result(...)` writes standard artifacts.
  4. Writes extra file: `expected_behavior.md`.
  5. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `ReplayChatCompletionClient`.
- Tools used: none.
- Expected input (`input_text.txt`):  
  `Explain what this repository demonstrates.`
- Expected final output (`example_output.txt`):  
  `AutoGen can orchestrate autonomous agents, tools, and workflows in a reusable way.`
- Extra artifacts: `expected_behavior.md`.
- `tool_calls.jsonl`: expected empty.

### 02_tools_file_explorer

- Runtime sequence:
  1. Resolves `data/documents` path via `get_project_paths()`.
  2. Builds `AssistantAgent` with `file_explorer_tools()`.
  3. First replay message is `tool_call_result(name="list_directory", ...)`.
  4. Agent returns final summary text.
  5. Writes standard artifacts + `expected_summary.json`.
  6. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `ReplayChatCompletionClient`, simulated `FunctionCall`.
- Tools used: `list_directory` (from `tools_fs.py`).
- Expected input:  
  `Inspect this directory and summarize what exists: ...\\AutoGen\\data\\documents`
- Expected final output:  
  `The folder contains two project files. Both are ready for downstream analysis.`
- Extra artifacts: `expected_summary.json`.
- `tool_calls.jsonl`: expected to include `list_directory`.

### 03_tools_text_analyzer

- Runtime sequence:
  1. Loads `quarterly_report.txt`.
  2. Builds `AssistantAgent` with `text_analysis_tools()`.
  3. Replays `tool_call_result(name="keyword_hits", ...)`.
  4. Returns business-signal summary.
  5. Writes standard artifacts + `analysis_expectations.json`.
  6. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `ReplayChatCompletionClient`, simulated `FunctionCall`.
- Tools used: `keyword_hits` (from `tools_text.py`).
- Expected input:  
  `Analyze the report and extract operational signals: ...\\quarterly_report.txt`
- Expected final output:  
  `Retention and revenue are strong, while onboarding delay is the key operational risk.`
- Extra artifacts: `analysis_expectations.json`.
- `tool_calls.jsonl`: expected to include `keyword_hits`.

### 04_multi_agent_handoff

- Runtime sequence:
  1. Builds `planner_agent` and `analyst_agent` as replay assistants.
  2. Wraps both in `RoundRobinGroupChat(max_turns=2)`.
  3. Executes team run via `run_agent_example(...)`.
  4. Writes standard artifacts + `handoff_structure.json`.
  5. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `RoundRobinGroupChat`, `ReplayChatCompletionClient`.
- Tools used: none.
- Expected input:  
  `Perform a simple planner-to-analyst handoff for the sample documents.`
- Expected final output:  
  `Execution result: risks = onboarding delay; actions = automate onboarding and segment tracking.`
- Extra artifacts: `handoff_structure.json`.
- `tool_calls.jsonl`: expected empty.

### 05_planner_executor

- Runtime sequence:
  1. Builds planner and executor assistants.
  2. Executor receives `file_explorer_tools()`.
  3. Team runs in `RoundRobinGroupChat(max_turns=2)`.
  4. Replay tool call: `list_text_files`.
  5. Writes standard artifacts + `plan_expectation.json`.
  6. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `RoundRobinGroupChat`, `ReplayChatCompletionClient`, simulated `FunctionCall`.
- Tools used: `list_text_files`.
- Expected input:  
  `Run planner/executor workflow for ...\\AutoGen\\data`
- Expected final output:  
  `Execution complete: text-like files were listed from the data folder.`
- Extra artifacts: `plan_expectation.json`.
- `tool_calls.jsonl`: expected to include `list_text_files`.

### 06_reflection_loop

- Runtime sequence:
  1. Builds one replay assistant with three sequential responses (draft/critique/final).
  2. Runs `assistant.run(...)` for draft.
  3. Runs `assistant.run(...)` for critique.
  4. Runs final step through `run_agent_example(...)`.
  5. Writes standard artifacts + `reflection_cycles.json`.
  6. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `ReplayChatCompletionClient`.
- Tools used: none.
- Expected input:  
  `Produce a revised final plan after reflection.`
- Expected final output:  
  `Draft v2: Build explorer + deterministic sample outputs + validation checklist.`
- Extra artifacts: `reflection_cycles.json`.
- `tool_calls.jsonl`: expected empty.

### 07_document_explorer

- Runtime sequence:
  1. Resolves target document path (`project_overview.txt`).
  2. Merges/deduplicates tool lists from file + text registries.
  3. Replays tool call `read_text_file`.
  4. Returns concise document-theme summary.
  5. Writes standard artifacts + `document_index.json`.
  6. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `ReplayChatCompletionClient`, simulated `FunctionCall`.
- Tools used: `read_text_file`.
- Expected input:  
  `Read and summarize this document: ...\\project_overview.txt`
- Expected final output:  
  `The document focuses on reusable tooling, OCR quality, and automation priorities.`
- Extra artifacts: `document_index.json`.
- `tool_calls.jsonl`: expected to include `read_text_file`.

### 08_batch_explorer

- Runtime sequence:
  1. Resolves metrics CSV and document folder.
  2. Builds assistant with `data_tools() + file_explorer_tools()`.
  3. Replays tool call `csv_head`.
  4. Runs main example through `run_agent_example(...)`.
  5. Post-processing step writes deterministic artifacts:
     - `batch_summary.csv`
     - `item_results.json`
     - `expected_behavior.md`
  6. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `ReplayChatCompletionClient`, simulated `FunctionCall`.
- Tools used: `csv_head`.
- Expected input:  
  `Prepare a batch summary using ...\\metrics.csv and document files.`
- Expected final output:  
  `Batch context loaded: metrics were previewed and are ready for per-file processing.`
- Extra artifacts: `batch_summary.csv`, `item_results.json`, `expected_behavior.md`.
- `tool_calls.jsonl`: expected to include `csv_head`.

### 09_human_in_the_loop

- Runtime sequence:
  1. `reviewer` agent proposes one action.
  2. Reads `HUMAN_APPROVAL` env var and decides branch.
  3. Approved branch:
     - `executor` with file tools,
     - replay tool call `list_directory`,
     - returns execution-complete message.
  4. Rejected branch:
     - no tools,
     - returns skip message.
  5. Writes standard artifacts + `human_decisions.json`.
  6. Runs standard output validation.
- AutoGen used: `AssistantAgent`, `ReplayChatCompletionClient`, simulated `FunctionCall` (approved branch).
- Tools used: `list_directory` (approved branch only).
- Expected input (approved baseline):  
  `Human approved. Execute the proposed action for: ...\\AutoGen\\data\\documents`
- Expected final output (approved baseline):  
  `Execution finished after human approval.`
- Extra artifacts: `human_decisions.json`.
- `tool_calls.jsonl`: non-empty when approved; empty when rejected.

### 10_conversational_coding_assistant

- Runtime sequence:
  1. Parses CLI args: `--mode` (`scripted` or `interactive`) and `--backend` (`replay`, `api`, `vllm`, or `ollama`).
  2. Builds assistant:
     - replay backend: `build_replay_assistant(...)`,
     - api/vLLM/Ollama backend: `build_live_assistant(...)` via backend-specific client.
  3. Scripted mode:
     - runs one deterministic coding task through `run_agent_example(...)`,
     - writes standard artifacts under `outputs/10_conversational_coding_assistant/`,
     - writes extras `session_config.json` and `usage_notes.md`,
     - runs standard output validation.
  4. Interactive mode:
     - loops user turns (`/help`, `/reset`, `/exit`),
     - runs `assistant.run(task=...)` per turn,
     - writes interactive artifacts under `outputs/10_conversational_coding_assistant_interactive/`.
- AutoGen used:
  - scripted replay: `AssistantAgent`, `ReplayChatCompletionClient`,
  - interactive live: `AssistantAgent`, OpenAI-compatible or Ollama live client.
- Tools used: none by default (chat-focused coding assistant).
- Expected input (scripted baseline):  
  `I am building a Python API endpoint for OCR jobs. Give me: 1) a minimal FastAPI endpoint, 2) a pydantic request model, 3) one validation rule, and 4) one test case idea.`
- Expected final output (scripted baseline):  
  concise coding plan + starter FastAPI code + one test idea.
- Extra artifacts (scripted): `session_config.json`, `usage_notes.md`.
- Local GPU knobs:
  - `--gpu-devices` configures `CUDA_VISIBLE_DEVICES`.
  - `--num-gpu`, `--num-ctx`, `--num-predict` configure Ollama runtime options.
