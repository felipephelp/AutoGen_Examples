# GitHub Workflow Flow (Detailed)

This flow describes the exact publish path for this workspace when targeting:
`https://github.com/felipephelp/AutoGen_Examples`.

```mermaid
flowchart TD
    %% Local preparation
    A0["Start in local repo<br/>C:/Users/fepac/Unicamp_Project/AutoGen"]:::entry
    A1["Edit files<br/>README, docs, examples, src"]:::process
    A2["Run local checks<br/>run_all_examples.ps1 or single example"]:::process
    A3["Inspect outputs/<example_id>/"]:::output
    A4{"Need more fixes?"}:::decision
    A5["Apply fixes and rerun"]:::process

    %% Git indexing and commit
    B1["git status --short"]:::module
    B2["git add <selected files>"]:::module
    B3["git commit -m '...'"]:::module
    B4{"Commit created?"}:::decision
    B5["Resolve commit issue<br/>empty stage/hooks/conflicts"]:::error

    %% Remote selection
    C1["git remote -v"]:::module
    C2{"Target remote = autogen_examples?"}:::decision
    C3["git push autogen_examples main"]:::module
    C4["Wrong target risk:<br/>origin may point to AutoGen"]:::error

    %% Push handling
    D1{"Push accepted?"}:::decision
    D2["Fix auth/permissions/network<br/>then retry push"]:::error
    D3["Remote main updated"]:::output

    %% GitHub side effects
    E1["GitHub repository: AutoGen_Examples"]:::entry
    E2["Commit appears in history<br/>hash, author, timestamp"]:::output
    E3["Files rendered on UI<br/>README Mermaid + docs Mermaid"]:::output
    E4["Clone/Pull consumers receive updates"]:::entry
    E5["Optional PR/Issues review cycle"]:::entry

    %% Sync checks
    F1["Optional verification commands:<br/>git ls-remote --heads autogen_examples<br/>git log --oneline -n 5"]:::module
    F2{"Remote and local aligned?"}:::decision
    F3["If not aligned: fetch/rebase/push again"]:::process
    F4["Publish complete"]:::entry

    %% Edges
    A0 --> A1 --> A2 --> A3 --> A4
    A4 -- "yes" --> A5 --> A2
    A4 -- "no" --> B1 --> B2 --> B3 --> B4
    B4 -- "no" --> B5 --> B1
    B4 -- "yes" --> C1 --> C2
    C2 -- "yes" --> C3 --> D1
    C2 -- "no" --> C4 --> C1
    D1 -- "no" --> D2 --> C3
    D1 -- "yes" --> D3 --> E1
    E1 --> E2
    E1 --> E3
    E2 --> E4
    E3 --> E5
    D3 --> F1 --> F2
    F2 -- "no" --> F3 --> C3
    F2 -- "yes" --> F4

    classDef entry fill:#E3F2FD,stroke:#1E88E5,color:#0D47A1,stroke-width:2px;
    classDef process fill:#E8F5E9,stroke:#43A047,color:#1B5E20,stroke-width:2px;
    classDef decision fill:#FFF8E1,stroke:#F9A825,color:#E65100,stroke-width:2px;
    classDef module fill:#E0F7FA,stroke:#00838F,color:#004D40,stroke-width:2px;
    classDef output fill:#EDE7F6,stroke:#5E35B1,color:#311B92,stroke-width:2px;
    classDef error fill:#FFEBEE,stroke:#E53935,color:#B71C1C,stroke-width:2px;
```

## Repository notes

- This workspace has multiple remotes; use `autogen_examples` when the target is `AutoGen_Examples`.
- Mermaid diagrams render directly in GitHub for both:
  - `docs/AUTOGEN_CALL_FLOW.md`
  - `docs/GITHUB_WORKFLOW_FLOW.md`
- Current repository does not include `.github/workflows/` CI automation.
