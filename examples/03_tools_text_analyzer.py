from __future__ import annotations

import asyncio

from _common import assert_standard_outputs, get_project_paths, write_extra_json
from autogen_infrastructure.agents_factory import build_replay_assistant
from autogen_infrastructure.model_client import tool_call_result
from autogen_infrastructure.orchestrators import run_agent_example
from autogen_infrastructure.tools_registry import text_analysis_tools


async def main() -> None:
    """Run keyword-based text-analysis example with tool-calling replay."""
    paths = get_project_paths()
    report_path = str(paths.data / "documents" / "quarterly_report.txt")
    report_text = (paths.data / "documents" / "quarterly_report.txt").read_text(
        encoding="utf-8", errors="ignore"
    )

    assistant = build_replay_assistant(
        name="text_analyzer_agent",
        responses=[
            tool_call_result(
                name="keyword_hits",
                arguments={"text": report_text, "keywords_csv": "revenue,cost,retention,onboarding"},
                call_id="keywords_1",
            ),
            "Retention and revenue are strong, while onboarding delay is the key operational risk.",
        ],
        tools=text_analysis_tools(),
        system_message="Use analysis tools and return concise business insights.",
    )

    _, package = await run_agent_example(
        example_id="03_tools_text_analyzer",
        task=f"Analyze the report and extract operational signals: {report_path}",
        runner=assistant,
        metadata={"example_type": "tool_calling_text", "source_file": report_path},
    )

    write_extra_json(
        package,
        "analysis_expectations.json",
        {
            "keywords": ["revenue", "cost", "retention", "onboarding"],
            "expected_focus": "onboarding delay as risk",
        },
    )
    missing = assert_standard_outputs("03_tools_text_analyzer")
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


if __name__ == "__main__":
    asyncio.run(main())
