from __future__ import annotations

import argparse
import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from _common import assert_standard_outputs, get_project_paths, write_extra_json, write_extra_markdown
from autogen_infrastructure.agents_factory import build_live_assistant, build_replay_assistant
from autogen_infrastructure.model_client import apply_local_gpu_config
from autogen_infrastructure.orchestrators import run_agent_example
from autogen_infrastructure.output_writer import write_json, write_jsonl, write_markdown, write_text

EXAMPLE_ID = "10_conversational_coding_assistant"

SYSTEM_PROMPT = (
    "You are a practical coding assistant. "
    "Help users design, write, refactor, and debug software with concise steps and runnable code examples."
)

SCRIPTED_TASK = (
    "I am building a Python API endpoint for OCR jobs. "
    "Give me: 1) a minimal FastAPI endpoint, 2) a pydantic request model, "
    "3) one validation rule, and 4) one test case idea."
)

SCRIPTED_REPLAY_RESPONSE = (
    "Plan:\\n"
    "1) Define a request schema with file_path and job_type.\\n"
    "2) Validate job_type against an allowlist.\\n"
    "3) Implement POST /ocr/jobs that enqueues work and returns job_id.\\n\\n"
    "Starter code:\\n"
    "```python\\n"
    "from fastapi import FastAPI, HTTPException\\n"
    "from pydantic import BaseModel, field_validator\\n\\n"
    "app = FastAPI()\\n\\n"
    "class OCRJobRequest(BaseModel):\\n"
    "    file_path: str\\n"
    "    job_type: str\\n\\n"
    "    @field_validator('job_type')\\n"
    "    @classmethod\\n"
    "    def validate_job_type(cls, value: str) -> str:\\n"
    "        allowed = {'invoice', 'receipt', 'report'}\\n"
    "        if value not in allowed:\\n"
    "            raise ValueError(f'job_type must be one of {sorted(allowed)}')\\n"
    "        return value\\n\\n"
    "@app.post('/ocr/jobs')\\n"
    "async def create_ocr_job(payload: OCRJobRequest):\\n"
    "    if not payload.file_path.strip():\\n"
    "        raise HTTPException(status_code=400, detail='file_path cannot be empty')\\n"
    "    return {'job_id': 'job_123', 'status': 'queued'}\\n"
    "```\\n\\n"
    "Test idea: send an invalid job_type and assert HTTP 422 validation error."
)

INTERACTIVE_REPLAY_RESPONSE = (
    "Replay mode response: this local interactive demo does not call a real LLM API. "
    "Switch to --backend api/vllm/ollama for dynamic answers."
)


def _content_to_text(content: Any) -> str:
    """Normalize assistant content to readable text."""
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False, indent=2)


def _resolved_model_label(args: argparse.Namespace) -> str:
    """Build a human-readable backend/model label for metadata and console."""
    if args.backend == "replay":
        return "replay"
    return f"{args.backend}:{args.model}"


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser for scripted and interactive conversational modes."""
    parser = argparse.ArgumentParser(
        prog="10_conversational_coding_assistant",
        description=(
            "Conversational coding assistant with replay(local), API, vLLM, and Ollama backends."
        ),
    )
    parser.add_argument("--mode", choices=["interactive", "scripted"], default="interactive")
    parser.add_argument("--backend", choices=["replay", "api", "vllm", "ollama"], default="replay")
    parser.add_argument("--model", default=os.getenv("AUTOGEN_LIVE_MODEL", "gpt-4o-mini"))
    parser.add_argument("--api-key", default=os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY"))
    parser.add_argument("--base-url", default=os.getenv("OPENAI_BASE_URL"))
    parser.add_argument("--vllm-base-url", default=os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1"))
    parser.add_argument("--ollama-host", default=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    parser.add_argument("--gpu-devices", default=os.getenv("AUTOGEN_GPU_DEVICES"))
    parser.add_argument("--num-gpu", type=int, default=None, help="Ollama-specific GPU count.")
    parser.add_argument("--num-ctx", type=int, default=None, help="Ollama context window override.")
    parser.add_argument("--num-predict", type=int, default=None, help="Ollama max prediction tokens.")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--max-turns", type=int, default=12)
    return parser


def _build_assistant(args: argparse.Namespace) -> Any:
    """Create assistant instance according to selected backend."""
    if args.backend == "replay":
        responses = [SCRIPTED_REPLAY_RESPONSE] if args.mode == "scripted" else [INTERACTIVE_REPLAY_RESPONSE] * 256
        return build_replay_assistant(
            name="coding_assistant",
            responses=responses,
            system_message=SYSTEM_PROMPT,
        )

    apply_local_gpu_config(cuda_visible_devices=args.gpu_devices)
    resolved_base_url = args.base_url
    if args.backend == "vllm":
        resolved_base_url = args.vllm_base_url

    return build_live_assistant(
        name="coding_assistant",
        backend=args.backend,
        model=args.model,
        api_key=args.api_key,
        base_url=resolved_base_url,
        ollama_host=args.ollama_host,
        system_message=SYSTEM_PROMPT,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        num_gpu=args.num_gpu,
        num_ctx=args.num_ctx,
        num_predict=args.num_predict,
    )


async def _run_scripted(args: argparse.Namespace) -> None:
    """Run deterministic one-turn scenario for expected outputs and CI-like checks."""
    assistant = _build_assistant(args)
    _, package = await run_agent_example(
        example_id=EXAMPLE_ID,
        task=SCRIPTED_TASK,
        runner=assistant,
        metadata={
            "example_type": "conversational_coding_assistant",
            "mode": "scripted",
            "backend": args.backend,
            "model": _resolved_model_label(args),
            "gpu_devices": args.gpu_devices,
            "num_gpu": args.num_gpu,
        },
    )

    write_extra_json(
        package,
        "session_config.json",
        {
            "mode": "scripted",
            "backend": args.backend,
            "model": _resolved_model_label(args),
            "gpu_devices": args.gpu_devices,
            "num_gpu": args.num_gpu,
            "num_ctx": args.num_ctx,
            "num_predict": args.num_predict,
            "system_prompt": SYSTEM_PROMPT,
            "task_profile": "single-turn coding assistant response",
        },
    )
    write_extra_markdown(
        package,
        "usage_notes.md",
        "- Scripted mode is deterministic and suitable for expected outputs.\n"
        "- Use interactive mode for multi-turn conversation.\n"
        "- Dynamic backends:\n"
        "  - `--backend api`: OpenAI-compatible remote API.\n"
        "  - `--backend vllm`: local/remote vLLM OpenAI-compatible endpoint.\n"
        "  - `--backend ollama`: local Ollama runtime.\n"
        "- Local GPU controls:\n"
        "  - `--gpu-devices` sets CUDA_VISIBLE_DEVICES.\n"
        "  - `--num-gpu` sets Ollama GPU usage.\n",
    )

    missing = assert_standard_outputs(EXAMPLE_ID)
    if missing:
        raise RuntimeError(f"Missing output files: {missing}")


def _build_interactive_transcript(turns: list[dict[str, str]]) -> str:
    """Render chat turns into markdown transcript."""
    lines = ["# Interactive Session Transcript", ""]
    for idx, turn in enumerate(turns, start=1):
        lines.append(f"## Turn {idx}")
        lines.append("### User")
        lines.append(turn["user"])
        lines.append("")
        lines.append("### Assistant")
        lines.append(turn["assistant"])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def _write_interactive_outputs(
    *,
    turns: list[dict[str, str]],
    args: argparse.Namespace,
    started_at: datetime,
) -> Path:
    """Persist interactive session artifacts in standard output shape."""
    paths = get_project_paths()
    out_dir = paths.outputs / f"{EXAMPLE_ID}_interactive"
    out_dir.mkdir(parents=True, exist_ok=True)

    input_text = "\n".join(f"[Turn {idx}] {t['user']}" for idx, t in enumerate(turns, start=1))
    final_output = turns[-1]["assistant"] if turns else ""
    transcript = _build_interactive_transcript(turns)

    write_json(
        out_dir / "run_metadata.json",
        {
            "example_id": f"{EXAMPLE_ID}_interactive",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "started_at_utc": started_at.isoformat(),
            "mode": "interactive",
            "backend": args.backend,
            "model": _resolved_model_label(args),
            "gpu_devices": args.gpu_devices,
            "num_gpu": args.num_gpu,
            "turn_count": len(turns),
            "stop_reason": "user_exit_or_max_turns",
        },
    )
    write_text(out_dir / "input_text.txt", input_text)
    write_text(out_dir / "example_output.txt", final_output)
    write_markdown(out_dir / "transcript.md", transcript)
    write_json(
        out_dir / "result.json",
        {
            "turns": turns,
            "last_assistant_message": final_output,
        },
    )
    write_jsonl(out_dir / "tool_calls.jsonl", [])
    write_json(
        out_dir / "session_config.json",
        {
            "mode": "interactive",
            "backend": args.backend,
            "model": _resolved_model_label(args),
            "max_turns": args.max_turns,
            "gpu_devices": args.gpu_devices,
            "num_gpu": args.num_gpu,
            "num_ctx": args.num_ctx,
            "num_predict": args.num_predict,
            "system_prompt": SYSTEM_PROMPT,
        },
    )
    return out_dir


async def _run_interactive(args: argparse.Namespace) -> None:
    """Run terminal chat loop and write a complete interactive session package."""
    assistant = _build_assistant(args)
    turns: list[dict[str, str]] = []
    started_at = datetime.now(timezone.utc)

    print("Conversational Coding Assistant")
    print("Commands: /help, /reset, /exit")
    print(f"Backend: {args.backend} | Model: {_resolved_model_label(args)}")
    if args.gpu_devices:
        print(f"CUDA_VISIBLE_DEVICES={args.gpu_devices}")

    turn_count = 0
    while turn_count < args.max_turns:
        user_text = input("you> ").strip()
        if not user_text:
            continue

        if user_text.lower() == "/exit":
            break
        if user_text.lower() == "/help":
            print("Type your coding question. Use /reset to clear local transcript. Use /exit to finish.")
            continue
        if user_text.lower() == "/reset":
            turns.clear()
            print("Local transcript cleared.")
            continue

        result = await assistant.run(task=user_text)
        assistant_text = ""
        if result.messages:
            assistant_text = _content_to_text(getattr(result.messages[-1], "content", ""))
        print(f"assistant> {assistant_text}")
        turns.append({"user": user_text, "assistant": assistant_text})
        turn_count += 1

    out_dir = _write_interactive_outputs(turns=turns, args=args, started_at=started_at)
    print(f"Interactive session saved to: {out_dir}")


async def main() -> None:
    """Entrypoint for scripted and interactive runs."""
    load_dotenv()
    args = build_parser().parse_args()

    try:
        if args.mode == "scripted":
            await _run_scripted(args)
            return

        await _run_interactive(args)
    except Exception as exc:  # noqa: BLE001
        if args.backend == "api":
            raise SystemExit(f"Live API execution failed: {exc}") from exc
        raise


if __name__ == "__main__":
    asyncio.run(main())
