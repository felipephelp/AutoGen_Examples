# AutoGen Examples

This repository provides **didactic AutoGen examples** for generic agent exploration workflows.
The code is split into:

- `src/autogen_infrastructure`: reusable infrastructure modules.
- `examples`: runnable scripts that demonstrate patterns progressively.

All tutorials and references are intentionally written in English.

## Project Layout

```text
AutoGen/
  data/
  docs/
  examples/
  outputs/
  samples/expected_outputs/
  scripts/
  src/autogen_infrastructure/
```

## Visual flowchart (GitHub)

GitHub renders Mermaid natively. For the complete flow with legend and branches, see:
`docs/AUTOGEN_CALL_FLOW.md`

For a detailed GitHub lifecycle flow (local changes -> commit -> push -> remote update), see:
`docs/GITHUB_WORKFLOW_FLOW.md`

Both documents are maintained in detailed mode with module/function-level steps.

For per-example operational flow (`01` to `10`) with expected input/output and AutoGen primitives used, see:
`docs/PER_EXAMPLE_EXECUTION_FLOW.md`

```mermaid
flowchart TD
    A["Entry<br/>run_all_examples.ps1 OR examples/*.py"]:::entry
    B{"Execution mode"}:::decision
    B1["Batch mode<br/>scripts/run_all_examples.ps1 loops 01..10"]:::module
    B2["Single mode<br/>python examples/0X_*.py"]:::module
    C["Bootstrap<br/>_common.py + get_project_paths()"]:::module
    D{"Which example?"}:::decision

    E01["01_basic_agent_chat<br/>Input: Explain repository demonstration<br/>Uses: AssistantAgent + Replay (no tools)<br/>Expected output: orchestration summary sentence"]:::example
    E02["02_tools_file_explorer<br/>Input: Inspect data/documents directory<br/>Uses: list_directory tool call<br/>Expected output: folder summary with 2 files"]:::example
    E03["03_tools_text_analyzer<br/>Input: Analyze quarterly_report.txt<br/>Uses: keyword_hits tool call<br/>Expected output: retention/revenue strong, onboarding risk"]:::example
    E04["04_multi_agent_handoff<br/>Input: planner-to-analyst handoff request<br/>Uses: RoundRobinGroupChat (planner + analyst)<br/>Expected output: risks/actions execution result"]:::example
    E05["05_planner_executor<br/>Input: run workflow for data folder<br/>Uses: RoundRobinGroupChat + list_text_files<br/>Expected output: text-like files listed completion message"]:::example
    E06["06_reflection_loop<br/>Input: produce revised final plan<br/>Uses: same agent across draft/critique/final<br/>Expected output: Draft v2 with validation checklist"]:::example
    E07["07_document_explorer<br/>Input: summarize project_overview.txt<br/>Uses: read_text_file tool call<br/>Expected output: tooling/OCR/automation themes"]:::example
    E08["08_batch_explorer<br/>Input: metrics.csv + documents batch request<br/>Uses: csv_head tool call + deterministic post-processing<br/>Expected output: batch context ready message"]:::example
    E09["09_human_in_the_loop<br/>Input: execute only if human approved<br/>Uses: HUMAN_APPROVAL gate + optional list_directory<br/>Expected output (approved baseline): execution finished"]:::example
    E10["10_conversational_coding_assistant<br/>Input: coding assistant request (scripted or interactive)<br/>Uses: replay(local), API, vLLM, or Ollama backend (+ optional GPU config)<br/>Expected output: coding plan + starter code response"]:::example

    F["Common runner<br/>run_agent_example(task, runner, metadata)"]:::process
    G["Result export<br/>export_task_result(...)"]:::module
    H["Standard outputs per example<br/>run_metadata, input_text, example_output,<br/>transcript, result, tool_calls"]:::output
    I["Example-specific extra files<br/>expected_behavior, plan_expectation,<br/>document_index, batch_summary, human_decisions, etc."]:::output
    J["Validation gate<br/>assert_standard_outputs -> validate_output_files"]:::module
    K{"Missing required files?"}:::decision
    L["RuntimeError (fail fast)"]:::error
    M["Compare with samples/expected_outputs/<example_id>"]:::output

    A --> B
    B -- "run_all_examples.ps1" --> B1 --> C
    B -- "single example script" --> B2 --> C
    C --> D
    D --> E01 --> F
    D --> E02 --> F
    D --> E03 --> F
    D --> E04 --> F
    D --> E05 --> F
    D --> E06 --> F
    D --> E07 --> F
    D --> E08 --> F
    D --> E09 --> F
    D --> E10 --> F
    F --> G --> H
    F --> I
    H --> J --> K
    K -- "Yes" --> L
    K -- "No" --> M

    classDef entry fill:#E3F2FD,stroke:#1E88E5,color:#0D47A1,stroke-width:2px;
    classDef process fill:#E8F5E9,stroke:#43A047,color:#1B5E20,stroke-width:2px;
    classDef decision fill:#FFF8E1,stroke:#F9A825,color:#E65100,stroke-width:2px;
    classDef module fill:#E0F7FA,stroke:#00838F,color:#004D40,stroke-width:2px;
    classDef output fill:#EDE7F6,stroke:#5E35B1,color:#311B92,stroke-width:2px;
    classDef example fill:#FFF3E0,stroke:#EF6C00,color:#BF360C,stroke-width:2px;
    classDef error fill:#FFEBEE,stroke:#E53935,color:#B71C1C,stroke-width:2px;
```

## Quick Start

From the `AutoGen` folder:

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pip install -e .
```

Run all examples:

```bash
.\scripts\run_all_examples.ps1
```

Run one example individually:

```bash
$env:PYTHONPATH = (Resolve-Path .\src)
.\.venv\Scripts\python.exe .\examples\05_planner_executor.py
```

Regenerate expected outputs:

```bash
.\scripts\regenerate_expected_outputs.ps1
```

## Example Matrix

| Example Script | Demonstrates | Infrastructure Modules Used | Expected Output Folder |
|---|---|---|---|
| `examples/01_basic_agent_chat.py` | Single agent baseline | `agents_factory.py`, `orchestrators.py`, `output_writer.py` | `samples/expected_outputs/01_basic_agent_chat/` |
| `examples/02_tools_file_explorer.py` | Tool-calling for file exploration | `tools_fs.py`, `tools_registry.py`, `model_client.py`, `agents_factory.py`, `orchestrators.py` | `samples/expected_outputs/02_tools_file_explorer/` |
| `examples/03_tools_text_analyzer.py` | Keyword-based text inspection | `tools_text.py`, `tools_registry.py`, `model_client.py`, `agents_factory.py`, `orchestrators.py` | `samples/expected_outputs/03_tools_text_analyzer/` |
| `examples/04_multi_agent_handoff.py` | Planner-to-analyst handoff | `agents_factory.py`, `orchestrators.py`, `output_writer.py` | `samples/expected_outputs/04_multi_agent_handoff/` |
| `examples/05_planner_executor.py` | Planner + executor with tools | `tools_fs.py`, `tools_registry.py`, `model_client.py`, `agents_factory.py`, `orchestrators.py` | `samples/expected_outputs/05_planner_executor/` |
| `examples/06_reflection_loop.py` | Self-critique and revision loop | `agents_factory.py`, `orchestrators.py`, `output_writer.py` | `samples/expected_outputs/06_reflection_loop/` |
| `examples/07_document_explorer.py` | Generic document exploration | `tools_fs.py`, `tools_text.py`, `tools_registry.py`, `model_client.py`, `agents_factory.py`, `orchestrators.py` | `samples/expected_outputs/07_document_explorer/` |
| `examples/08_batch_explorer.py` | Batch pipeline with deterministic summaries | `tools_data.py`, `tools_fs.py`, `tools_registry.py`, `model_client.py`, `agents_factory.py`, `orchestrators.py`, `output_writer.py` | `samples/expected_outputs/08_batch_explorer/` |
| `examples/09_human_in_the_loop.py` | Human approval gate before execution | `tools_fs.py`, `tools_registry.py`, `model_client.py`, `agents_factory.py`, `orchestrators.py` | `samples/expected_outputs/09_human_in_the_loop/` |
| `examples/10_conversational_coding_assistant.py` | Chat-style coding assistant (scripted + interactive; replay/API/vLLM/Ollama) | `model_client.py`, `agents_factory.py`, `orchestrators.py`, `output_writer.py` | `samples/expected_outputs/10_conversational_coding_assistant/` |

## What to Expect in Each Output Folder

Every example writes:

- `run_metadata.json`: run metadata (example id, timestamp, message count, stop reason).
- `input_text.txt`: exact input task sent to the example run.
- `example_output.txt`: final output produced by the example (last message content).
- `transcript.md`: full conversational trace in readable markdown.
- `result.json`: structured message payloads for programmatic inspection.
- `tool_calls.jsonl`: tool call request/execution events (empty for non-tool examples).

### Output Files Reference

| File | Purpose | Typical Use |
|---|---|---|
| `run_metadata.json` | Technical metadata about a run | Auditing, reproducibility checks |
| `input_text.txt` | Input prompt/task used in execution | Understand expected scenario and replay context |
| `example_output.txt` | Final answer produced by the example | Quick â€œwhat should I expectâ€ check |
| `transcript.md` | Full step-by-step conversation | Debugging agent flow and reasoning sequence |
| `result.json` | Structured representation of all messages | Automated assertions and downstream processing |
| `tool_calls.jsonl` | Tool call request/execution records | Validate tool usage and arguments |

Some examples also add custom files:

- `expected_behavior.md`
- `expected_summary.json`
- `analysis_expectations.json`
- `handoff_structure.json`
- `plan_expectation.json`
- `reflection_cycles.json`
- `document_index.json`
- `batch_summary.csv`
- `item_results.json`
- `human_decisions.json`
- `session_config.json`
- `usage_notes.md`

## Why `examples` and `autogen_infrastructure` are separate

- `autogen_infrastructure` centralizes reusable components.
- `examples` stay short and focused on teaching one concept each.
- The separation avoids code duplication and improves maintainability.

## References

- AutoGen official repository: https://github.com/microsoft/autogen
