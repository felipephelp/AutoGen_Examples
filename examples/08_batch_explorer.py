from __future__ import annotations

import asyncio
import csv
from pathlib import Path

from _common import assert_standard_outputs, get_project_paths, write_extra_json
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.model_client import tool_call_result
from autogen_infrastructure.orchestrators import run_agent_example
from autogen_infrastructure.output_writer import write_markdown
from autogen_infrastructure.tools_registry import data_tools, file_explorer_tools


async def main() -> None:
    paths = get_project_paths()
    csv_path = str(paths.data / "notes" / "metrics.csv")
    data_dir = paths.data / "documents"

    assistant = build_replay_assistant(
        name="batch_explorer",
        responses=[
            tool_call_result(name="csv_head", arguments={"path": csv_path, "rows": 5}, call_id="csv_preview"),
            "Batch context loaded: metrics were previewed and are ready for per-file processing.",
        ],
        tools=data_tools() + file_explorer_tools(),
        system_message="Prepare batch processing context before summarizing.",
    )

    _, package = await run_agent_example(
        example_id="08_batch_explorer",
        task=f"Prepare a batch summary using {csv_path} and document files.",
        runner=assistant,
        metadata={"example_type": "batch_pipeline", "metrics_csv": csv_path},
    )

    documents = sorted([p for p in data_dir.glob("*.txt") if p.is_file()])
    rows: list[dict[str, str | int]] = []
    for p in documents:
        text = p.read_text(encoding="utf-8", errors="ignore")
        rows.append(
            {
                "file": p.name,
                "characters": len(text),
                "lines": len(text.splitlines()),
            }
        )

    out_dir = Path(package["output_dir"])
    csv_out = out_dir / "batch_summary.csv"
    with csv_out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "characters", "lines"])
        writer.writeheader()
        writer.writerows(rows)

    write_extra_json(package, "item_results.json", rows)
    write_markdown(
        out_dir / "expected_behavior.md",
        "- Metrics CSV is previewed through a tool call.\n"
        "- A deterministic `batch_summary.csv` is generated for all text files.\n",
    )

    missing = assert_standard_outputs("08_batch_explorer")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
