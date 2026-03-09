from __future__ import annotations

import asyncio

from _common import assert_standard_outputs, get_project_paths, write_extra_json
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.model_client import tool_call_result
from autogen_infrastructure.orchestrators import run_agent_example
from autogen_infrastructure.tools_registry import file_explorer_tools, text_analysis_tools


async def main() -> None:
    paths = get_project_paths()
    doc_path = str(paths.data / "documents" / "project_overview.txt")

    tools_by_name = {}
    for tool in file_explorer_tools() + text_analysis_tools():
        tools_by_name[tool.__name__] = tool
    tools = list(tools_by_name.values())
    assistant = build_replay_assistant(
        name="document_explorer",
        responses=[
            tool_call_result(
                name="read_text_file",
                arguments={"path": doc_path},
                call_id="read_overview",
            ),
            "The document focuses on reusable tooling, OCR quality, and automation priorities.",
        ],
        tools=tools,
        system_message="Explore documents and extract actionable themes.",
    )

    _, package = await run_agent_example(
        example_id="07_document_explorer",
        task=f"Read and summarize this document: {doc_path}",
        runner=assistant,
        metadata={"example_type": "document_explorer", "document": doc_path},
    )

    write_extra_json(
        package,
        "document_index.json",
        {
            "documents": [
                str(paths.data / "documents" / "project_overview.txt"),
                str(paths.data / "documents" / "quarterly_report.txt"),
            ],
            "focus_themes": ["tooling", "ocr quality", "automation"],
        },
    )
    missing = assert_standard_outputs("07_document_explorer")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
