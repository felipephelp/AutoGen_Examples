# GitHub Workflow Flow (Detailed)

This flow describes what happens from local development to repository updates in GitHub (`AutoGen_Examples`).

```mermaid
flowchart TD
    subgraph LOCAL["Local workspace (VS Code + terminal)"]
        A1["Edit code/docs<br/>examples/, src/, docs/, scripts/"]:::process
        A2["Run validation<br/>run_all_examples.ps1 or individual examples"]:::process
        A3["Generate outputs<br/>outputs/<example_id>/..."]:::output
        A4{"Outputs valid?"}:::decision
        A5["Adjust code and re-run"]:::process
        A6["Stage files<br/>git add ..."]:::module
        A7["Create commit<br/>git commit -m '...'"]:::module
    end

    subgraph GIT["Git transport"]
        B1["Push branch<br/>git push autogen_examples main"]:::module
        B2{"Push accepted?"}:::decision
        B3["Fix auth/conflicts and retry"]:::error
    end

    subgraph GH["GitHub: felipephelp/AutoGen_Examples"]
        C1["Remote branch updated<br/>main receives new commit"]:::output
        C2["Repository files updated<br/>README, docs, src, examples, samples"]:::output
        C3["History updated<br/>commit hash + diff + timestamp"]:::output
        C4["Consumers pull changes<br/>git pull / clone"]:::entry
        C5["Optional collaboration<br/>issues, PRs, review comments"]:::entry
    end

    A1 --> A2 --> A3 --> A4
    A4 -- "No" --> A5 --> A2
    A4 -- "Yes" --> A6 --> A7 --> B1 --> B2
    B2 -- "No" --> B3 --> B1
    B2 -- "Yes" --> C1 --> C2 --> C3
    C3 --> C4
    C2 --> C5

    classDef entry fill:#E3F2FD,stroke:#1E88E5,color:#0D47A1,stroke-width:2px;
    classDef process fill:#E8F5E9,stroke:#43A047,color:#1B5E20,stroke-width:2px;
    classDef decision fill:#FFF8E1,stroke:#F9A825,color:#E65100,stroke-width:2px;
    classDef module fill:#E0F7FA,stroke:#00838F,color:#004D40,stroke-width:2px;
    classDef output fill:#EDE7F6,stroke:#5E35B1,color:#311B92,stroke-width:2px;
    classDef error fill:#FFEBEE,stroke:#E53935,color:#B71C1C,stroke-width:2px;
```

## What this repository currently does on GitHub

- Stores deterministic examples and expected outputs for reproducibility.
- Tracks documentation updates (`README`, `docs/*`) and infrastructure code (`src/*`).
- Does not currently include a `.github/workflows/` CI pipeline in this repository.
