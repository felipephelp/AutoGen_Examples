# Outputs Reference

All examples generate output in:

```text
outputs/<example_id>/
```

Reference snapshots are versioned in:

```text
samples/expected_outputs/<example_id>/
```

## Standard files

- `run_metadata.json`
- `transcript.md`
- `result.json`
- `tool_calls.jsonl`

## Custom files by example

- `01_basic_agent_chat`: `expected_behavior.md`
- `02_tools_file_explorer`: `expected_summary.json`
- `03_tools_text_analyzer`: `analysis_expectations.json`
- `04_multi_agent_handoff`: `handoff_structure.json`
- `05_planner_executor`: `plan_expectation.json`
- `06_reflection_loop`: `reflection_cycles.json`
- `07_document_explorer`: `document_index.json`
- `08_batch_explorer`: `batch_summary.csv`, `item_results.json`, `expected_behavior.md`
- `09_human_in_the_loop`: `human_decisions.json`
