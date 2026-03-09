# AutoGen Runtime Call Flow (Detailed)

This diagram shows the full runtime path inside `AutoGen_Examples`, including:
- launch modes (`run_all_examples.ps1` vs single script),
- infrastructure function calls,
- tool-calling/replay behavior,
- output files and validation gates.

For per-example operational detail (what happens in each `01..10`, expected input/output, and AutoGen primitives), see:
`docs/PER_EXAMPLE_EXECUTION_FLOW.md`

## Mermaid flowchart

```mermaid
flowchart TD
    %% Launch layer
    A0["Developer command<br/>./scripts/run_all_examples.ps1"]:::entry
    A1["or<br/>python examples/0X_example.py"]:::entry
    A2{"Launch mode"}:::decision
    A3["PowerShell loop:<br/>run examples 01..10 in order"]:::module
    A4["Single script executes directly"]:::module

    %% Bootstrap layer
    B1["examples/_common.py<br/>injects src into sys.path"]:::module
    B2["get_project_paths()<br/>resolve root/data/docs/outputs"]:::module
    B3["Example declares:<br/>task, responses, metadata"]:::process

    %% Agent/model build layer
    C1["agents_factory.build_replay_assistant(...)"]:::module
    C2["model_client.create_replay_client(...)"]:::module
    C3["ReplayChatCompletionClient<br/>model_info.function_calling = bool(tools)"]:::module
    C4{"Tools used by this example?"}:::decision
    C5["tools_registry.*()<br/>file/text/data tool sets"]:::module
    C6["model_client.tool_call_result(...)<br/>CreateResult(FunctionCall)"]:::module
    C7{"Runner type"}:::decision
    C8["AssistantAgent"]:::module
    C9["RoundRobinGroupChat<br/>(planner/executor or handoff)"]:::module

    %% Execution layer
    D1["orchestrators.run_agent_example(...)"]:::process
    D2["runner.run(task=...)"]:::process
    D3["elapsed_seconds measured"]:::process
    D4["optional console summary<br/>AUTOGEN_EXAMPLE_CONSOLE"]:::process
    D5["Replay-mode warnings may appear:<br/>tool_choice ignored / token count note"]:::error

    %% Output writer layer
    E1["output_writer.export_task_result(...)"]:::module
    E2["_message_to_row + _build_transcript"]:::module
    E3["Write base artifacts"]:::output
    E4["outputs/<example_id>/run_metadata.json"]:::output
    E5["outputs/<example_id>/input_text.txt"]:::output
    E6["outputs/<example_id>/example_output.txt"]:::output
    E7["outputs/<example_id>/transcript.md"]:::output
    E8["outputs/<example_id>/result.json"]:::output
    E9["outputs/<example_id>/tool_calls.jsonl"]:::output

    %% Example-specific extras
    F1["Example writes extra files (optional)"]:::output
    F2["expected_behavior.md / expected_summary.json"]:::output
    F3["plan_expectation.json / reflection_cycles.json"]:::output
    F4["document_index.json / item_results.json / batch_summary.csv"]:::output
    F5["human_decisions.json / handoff_structure.json"]:::output

    %% Validation layer
    G1["assert_standard_outputs(example_id)"]:::module
    G2["validators.validate_output_files(...)"]:::module
    G3{"Any required file missing/empty?"}:::decision
    G4["raise RuntimeError"]:::error
    G5["Example run considered successful"]:::entry

    %% Reference baseline
    H1["samples/expected_outputs/<example_id>/"]:::output
    H2["Manual compare or regenerate script"]:::process

    %% Edges
    A0 --> A2
    A1 --> A2
    A2 -- "run_all" --> A3 --> B1
    A2 -- "single" --> A4 --> B1
    B1 --> B2 --> B3 --> C1 --> C2 --> C3 --> C4
    C4 -- "yes" --> C5 --> C6 --> C7
    C4 -- "no" --> C7
    C7 -- "single agent" --> C8 --> D1
    C7 -- "team chat" --> C9 --> D1
    D1 --> D2 --> D3 --> D4
    D2 -. replay runtime notes .-> D5
    D3 --> E1 --> E2 --> E3
    E3 --> E4
    E3 --> E5
    E3 --> E6
    E3 --> E7
    E3 --> E8
    E3 --> E9
    B3 --> F1
    F1 --> F2
    F1 --> F3
    F1 --> F4
    F1 --> F5
    E4 --> G1
    E5 --> G1
    E6 --> G1
    E7 --> G1
    E8 --> G1
    E9 --> G1
    G1 --> G2 --> G3
    G3 -- "yes" --> G4
    G3 -- "no" --> G5
    G5 --> H1 --> H2

    subgraph LEGEND["Legend"]
        L1["Input / Entry"]:::entry
        L2["Processing step"]:::process
        L3{"Decision"}:::decision
        L4["Module / Integration"]:::module
        L5["Output artifact"]:::output
        L6["Warning / Error path"]:::error
    end

    classDef entry fill:#E3F2FD,stroke:#1E88E5,color:#0D47A1,stroke-width:2px;
    classDef process fill:#E8F5E9,stroke:#43A047,color:#1B5E20,stroke-width:2px;
    classDef decision fill:#FFF8E1,stroke:#F9A825,color:#E65100,stroke-width:2px;
    classDef module fill:#E0F7FA,stroke:#00838F,color:#004D40,stroke-width:2px;
    classDef output fill:#EDE7F6,stroke:#5E35B1,color:#311B92,stroke-width:2px;
    classDef error fill:#FFEBEE,stroke:#E53935,color:#B71C1C,stroke-width:2px;
```

## Notes

- Current model mode: replay/mock (`ReplayChatCompletionClient`), deterministic for didactic use.
- Tool-calling examples are simulated by replayed `FunctionCall` messages.
- Base outputs are always under `outputs/<example_id>/`.
- Reference outputs remain under `samples/expected_outputs/<example_id>/`.
