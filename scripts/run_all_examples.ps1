$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root
$env:PYTHONPATH = (Join-Path $root "src")
$env:AUTOGEN_EXAMPLE_CONSOLE = "0"

$examples = @(
  "01_basic_agent_chat.py",
  "02_tools_file_explorer.py",
  "03_tools_text_analyzer.py",
  "04_multi_agent_handoff.py",
  "05_planner_executor.py",
  "06_reflection_loop.py",
  "07_document_explorer.py",
  "08_batch_explorer.py",
  "09_human_in_the_loop.py",
  "10_conversational_coding_assistant.py"
)

foreach ($example in $examples) {
  Write-Host "Running $example"
  $previousPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  $examplePath = (Join-Path "examples" $example)
  if ($example -eq "10_conversational_coding_assistant.py") {
    $rawLogs = & ".\.venv\Scripts\python.exe" $examplePath "--mode" "scripted" "--backend" "replay" 2>&1
  } else {
    $rawLogs = & ".\.venv\Scripts\python.exe" $examplePath 2>&1
  }
  $exitCode = $LASTEXITCODE
  $ErrorActionPreference = $previousPreference

  $noisePatterns = @(
    "tool_choice parameter specified but is ignored in replay mode",
    "Token count has been done only on string content"
  )
  $cleanLogs = @()
  foreach ($lineObj in $rawLogs) {
    $line = [string]$lineObj
    $isNoise = $false
    foreach ($pattern in $noisePatterns) {
      if ($line -like "*$pattern*") {
        $isNoise = $true
        break
      }
    }
    if (-not $isNoise -and -not [string]::IsNullOrWhiteSpace($line)) {
      $cleanLogs += $line
    }
  }

  if ($exitCode -ne 0) {
    Write-Host "[$example] Execution failed. Raw logs:"
    foreach ($lineObj in $rawLogs) {
      Write-Host ([string]$lineObj)
    }
    throw "Example failed: $example"
  }

  if ($cleanLogs.Count -gt 0) {
    Write-Host "[$example] Additional logs:"
    foreach ($line in $cleanLogs) {
      Write-Host $line
    }
  }

  $exampleId = [System.IO.Path]::GetFileNameWithoutExtension($example)
  $outDir = Join-Path $root ("outputs\" + $exampleId)
  $inputFile = Join-Path $outDir "input_text.txt"
  $outputFile = Join-Path $outDir "example_output.txt"

  if (Test-Path $inputFile) {
    $inputText = Get-Content $inputFile -Raw
    Write-Host "[$exampleId] INPUT_TEXT"
    Write-Host $inputText
  } else {
    Write-Warning "[$exampleId] Missing input file: $inputFile"
  }

  if (Test-Path $outputFile) {
    $outputText = Get-Content $outputFile -Raw
    Write-Host "[$exampleId] EXAMPLE_OUTPUT"
    Write-Host $outputText
  } else {
    Write-Warning "[$exampleId] Missing output file: $outputFile"
  }

  Write-Host "----------------------------------------"
}
