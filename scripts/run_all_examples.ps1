$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root
$env:PYTHONPATH = (Join-Path $root "src")

$examples = @(
  "01_basic_agent_chat.py",
  "02_tools_file_explorer.py",
  "03_tools_text_analyzer.py",
  "04_multi_agent_handoff.py",
  "05_planner_executor.py",
  "06_reflection_loop.py",
  "07_document_explorer.py",
  "08_batch_explorer.py",
  "09_human_in_the_loop.py"
)

foreach ($example in $examples) {
  Write-Host "Running $example"
  & ".\.venv\Scripts\python.exe" (Join-Path "examples" $example)
  if ($LASTEXITCODE -ne 0) {
    throw "Example failed: $example"
  }
}
