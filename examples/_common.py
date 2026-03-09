from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from autogen_infrastructure.config import get_project_paths  # noqa: E402
from autogen_infrastructure.output_writer import write_json, write_markdown  # noqa: E402
from autogen_infrastructure.validators import validate_output_files  # noqa: E402


def output_dir_from_package(package: dict[str, Any]) -> Path:
    return Path(package["output_dir"])


def write_extra_json(package: dict[str, Any], filename: str, payload: Any) -> Path:
    path = output_dir_from_package(package) / filename
    write_json(path, payload)
    return path


def write_extra_markdown(package: dict[str, Any], filename: str, content: str) -> Path:
    path = output_dir_from_package(package) / filename
    write_markdown(path, content)
    return path


def assert_standard_outputs(example_id: str) -> list[str]:
    paths = get_project_paths()
    out_dir = paths.outputs / example_id
    return validate_output_files(
        out_dir,
        [
            "run_metadata.json",
            "input_text.txt",
            "example_output.txt",
            "transcript.md",
            "result.json",
            "tool_calls.jsonl",
        ],
    )
