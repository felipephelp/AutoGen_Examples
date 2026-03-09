from __future__ import annotations

from pathlib import Path


def list_directory(path: str, max_entries: int = 50) -> str:
    """List directory entries with a compact type marker."""
    target = Path(path).expanduser().resolve()
    if not target.exists():
        return f"[ERROR] Path not found: {target}"
    if not target.is_dir():
        return f"[ERROR] Not a directory: {target}"

    entries = sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    lines = [f"Directory: {target}"]
    for item in entries[:max_entries]:
        marker = "[D]" if item.is_dir() else "[F]"
        lines.append(f"{marker} {item.name}")

    if len(entries) > max_entries:
        lines.append(f"... truncated {len(entries) - max_entries} entries")
    return "\n".join(lines)


def list_text_files(path: str, recursive: bool = True, max_entries: int = 200) -> str:
    """List text-like files under a directory for exploration tasks."""
    target = Path(path).expanduser().resolve()
    if not target.exists():
        return f"[ERROR] Path not found: {target}"
    if not target.is_dir():
        return f"[ERROR] Not a directory: {target}"

    allowed = {".txt", ".md", ".csv", ".json", ".py"}
    iterator = target.rglob("*") if recursive else target.glob("*")
    files = [p for p in iterator if p.is_file() and p.suffix.lower() in allowed]
    files.sort(key=lambda p: p.as_posix().lower())

    lines = [f"Text-like files in: {target}"]
    for p in files[:max_entries]:
        lines.append(str(p))
    if len(files) > max_entries:
        lines.append(f"... truncated {len(files) - max_entries} files")
    return "\n".join(lines)


def read_text_file(path: str, max_chars: int = 6000) -> str:
    """Read text file content with optional truncation."""
    target = Path(path).expanduser().resolve()
    if not target.exists():
        return f"[ERROR] File not found: {target}"
    if not target.is_file():
        return f"[ERROR] Not a file: {target}"

    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text) > max_chars:
        return text[:max_chars] + f"\n\n[TRUNCATED at {max_chars} chars]"
    return text
