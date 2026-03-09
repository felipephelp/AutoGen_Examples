$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

& (Join-Path $PSScriptRoot "run_all_examples.ps1")

$expected = Join-Path $root "samples\expected_outputs"
if (Test-Path $expected) {
  Remove-Item -Recurse -Force $expected
}
New-Item -ItemType Directory -Force -Path $expected | Out-Null

$outputDirs = Get-ChildItem -Path (Join-Path $root "outputs") -Directory
foreach ($dir in $outputDirs) {
  Copy-Item -Recurse -Force $dir.FullName (Join-Path $expected $dir.Name)
}
Write-Host "Expected outputs refreshed at $expected"
