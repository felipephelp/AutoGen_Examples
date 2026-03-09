from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from autogen_agentchat.base import TaskResult

from .config import get_project_paths


def _to_jsonable(value: Any) -> Any:
    """Convert rich runtime objects to JSON-serializable structures."""
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_jsonable(v) for v in value]
    if hasattr(value, "model_dump"):
        return _to_jsonable(value.model_dump(mode="json"))
    if hasattr(value, "__dict__"):
        return _to_jsonable(vars(value))
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    """Write JSON payload to disk creating parent directories when needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_to_jsonable(payload), indent=2), encoding="utf-8")


def write_markdown(path: Path, content: str) -> None:
    """Write markdown text to disk creating parent directories when needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """Write plain text to disk creating parent directories when needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write list of dict rows as JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(_to_jsonable(row), ensure_ascii=False) + "\n")


def _message_to_row(message: Any) -> dict[str, Any]:
    """Normalize agent message object into serializable row format."""
    return {
        "message_type": type(message).__name__,
        "source": getattr(message, "source", ""),
        "content": _to_jsonable(getattr(message, "content", None)),
    }


def _build_transcript(messages: list[Any]) -> str:
    """Build markdown transcript from ordered message list."""
    chunks: list[str] = []
    for msg in messages:
        row = _message_to_row(msg)
        chunks.append(f"## {row['source'] or 'unknown'} ({row['message_type']})")
        content = row["content"]
        if isinstance(content, str):
            chunks.append(content)
        else:
            chunks.append("```json\n" + json.dumps(content, indent=2, ensure_ascii=False) + "\n```")
        chunks.append("")
    return "\n".join(chunks).strip() + "\n"


def export_task_result(
    *,
    example_id: str,
    task: str,
    result: TaskResult,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Export canonical output files for one example execution."""
    paths = get_project_paths()
    out_dir = paths.outputs / example_id
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [_message_to_row(msg) for msg in result.messages]
    final_row = rows[-1] if rows else {}
    tool_rows = [r for r in rows if "ToolCall" in r["message_type"]]
    final_output = final_row.get("content", "")
    if not isinstance(final_output, str):
        final_output = json.dumps(final_output, indent=2, ensure_ascii=False)

    write_json(
        out_dir / "run_metadata.json",
        {
            "example_id": example_id,
            "task": task,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "message_count": len(rows),
            "stop_reason": getattr(result, "stop_reason", None),
            **(metadata or {}),
        },
    )
    write_text(out_dir / "input_text.txt", task)
    write_text(out_dir / "example_output.txt", final_output)
    write_markdown(out_dir / "transcript.md", _build_transcript(result.messages))
    write_json(out_dir / "result.json", {"final_message": final_row, "all_messages": rows})
    write_jsonl(out_dir / "tool_calls.jsonl", tool_rows)

    package = {
        "output_dir": str(out_dir),
        "run_metadata": str(out_dir / "run_metadata.json"),
        "input_text": str(out_dir / "input_text.txt"),
        "example_output": str(out_dir / "example_output.txt"),
        "transcript": str(out_dir / "transcript.md"),
        "result": str(out_dir / "result.json"),
        "tool_calls": str(out_dir / "tool_calls.jsonl"),
    }
    return package
