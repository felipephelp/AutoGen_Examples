from __future__ import annotations

from pathlib import Path


def validate_output_files(output_dir: Path, expected_files: list[str]) -> list[str]:
    """Return missing/empty expected files for an output directory."""
    missing: list[str] = []
    for filename in expected_files:
        path = output_dir / filename
        if not path.exists():
            missing.append(str(path))
            continue
        # tool_calls can legitimately be empty for non-tool examples.
        if filename == "tool_calls.jsonl":
            continue
        if path.is_file() and not path.read_text(encoding="utf-8", errors="ignore").strip():
            missing.append(str(path) + " (empty)")
    return missing
