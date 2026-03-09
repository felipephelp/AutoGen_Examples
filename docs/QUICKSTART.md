# Quickstart

1. Create environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m pip install -e .
```

2. Run one example:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src)
.\.venv\Scripts\python.exe .\examples\02_tools_file_explorer.py
```

3. Inspect generated outputs:

```text
outputs/02_tools_file_explorer/
```
