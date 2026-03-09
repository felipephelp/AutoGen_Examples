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

## Quick Start

From the `AutoGen` folder:

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python -m pip install -e .
```

Run all examples:

```bash
.\scripts\run_all_examples.ps1
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

## What to Expect in Each Output Folder

Every example writes:

- `run_metadata.json`: execution metadata.
- `transcript.md`: conversational trace.
- `result.json`: final and intermediate messages.
- `tool_calls.jsonl`: only tool call request/execution events.

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

## Why `examples` and `autogen_infrastructure` are separate

- `autogen_infrastructure` centralizes reusable components.
- `examples` stay short and focused on teaching one concept each.
- The separation avoids code duplication and improves maintainability.

## References

- AutoGen official repository: https://github.com/microsoft/autogen
