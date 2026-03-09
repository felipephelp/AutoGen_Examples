from __future__ import annotations

import csv
from pathlib import Path


def csv_head(path: str, rows: int = 5) -> str:
    target = Path(path).expanduser().resolve()
    if not target.exists():
        return f"[ERROR] File not found: {target}"
    if target.suffix.lower() != ".csv":
        return f"[ERROR] Expected CSV file: {target}"

    lines: list[str] = []
    with target.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            lines.append(", ".join(row))
            if i + 1 >= rows:
                break
    return "\n".join(lines)
