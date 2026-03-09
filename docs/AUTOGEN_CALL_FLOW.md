# AutoGen Call Flow

This document explains the runtime chain of `AutoGen` examples and where outputs are produced.

## Mermaid flowchart

```mermaid
flowchart TD
    A["Input / Entry<br/>scripts/run_all_examples.ps1<br/>or python examples/<file>.py"]:::entry
    A1["PowerShell orchestrates sequential execution (optional)"]:::module
    B["examples/_common.py<br/>adds src to PYTHONPATH and helper writers"]:::module
    C["Example script (01..09)<br/>defines task + replay responses + metadata"]:::process
    D["agents_factory.build_replay_assistant(...)"]:::module
    D1["model_client.create_replay_client(...)"]:::module
    E{"Tool-calling example?"}:::decision
    F["tools_registry + tools_fs/tools_text/tools_data"]:::module
    F1["model_client.tool_call_result(...)"]:::module
    G["orchestrators.run_agent_example(...)"]:::process
    H["runner.run(task=...)<br/>AssistantAgent or GroupChat"]:::process
    I["output_writer.export_task_result(...)"]:::module

    O1["outputs/<example_id>/run_metadata.json"]:::output
    O2["outputs/<example_id>/input_text.txt"]:::output
    O3["outputs/<example_id>/example_output.txt"]:::output
    O4["outputs/<example_id>/transcript.md"]:::output
    O5["outputs/<example_id>/result.json"]:::output
    O6["outputs/<example_id>/tool_calls.jsonl"]:::output
    O7["extra files per example<br/>plan_expectation.json, document_index.json, etc."]:::output
    O8["samples/expected_outputs/<example_id>/ baseline"]:::output

    V1["validators.assert_standard_outputs(...)"]:::module
    V2{"Missing files?"}:::decision
    ERR["raise RuntimeError"]:::error
    END["Console summary per example"]:::entry

    A --> A1 --> C
    A --> B --> C
    C --> D --> D1 --> E
    E -- "Yes" --> F --> F1 --> G
    E -- "No" --> G
    G --> H --> I
    I --> O1
    I --> O2
    I --> O3
    I --> O4
    I --> O5
    I --> O6
    C --> O7
    O1 --> V1
    O2 --> V1
    O3 --> V1
    O4 --> V1
    O5 --> V1
    O6 --> V1
    V1 --> V2
    V2 -- "Yes" --> ERR
    V2 -- "No" --> END
    O8 --- V1

    subgraph LEGEND["Legend"]
        L1["Input / Entry"]:::entry
        L2["Processing step"]:::process
        L3{"Decision"}:::decision
        L4["Module / Integration"]:::module
        L5["Output data artifact"]:::output
        L6["Error path"]:::error
    end

    classDef entry fill:#E3F2FD,stroke:#1E88E5,color:#0D47A1,stroke-width:2px;
    classDef process fill:#E8F5E9,stroke:#43A047,color:#1B5E20,stroke-width:2px;
    classDef decision fill:#FFF8E1,stroke:#F9A825,color:#E65100,stroke-width:2px;
    classDef module fill:#E0F7FA,stroke:#00838F,color:#004D40,stroke-width:2px;
    classDef output fill:#EDE7F6,stroke:#5E35B1,color:#311B92,stroke-width:2px;
    classDef error fill:#FFEBEE,stroke:#E53935,color:#B71C1C,stroke-width:2px;
```

## Notes

- Current model mode in this repository is replay/mock (`ReplayChatCompletionClient`).
- Tool-capable examples simulate tool calls with deterministic responses.
- `outputs/` contains the current run; `samples/expected_outputs/` is versioned reference data.
