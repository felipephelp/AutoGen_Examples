from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProjectPaths:
    root: Path
    src: Path
    examples: Path
    docs: Path
    outputs: Path
    samples_expected_outputs: Path
    data: Path

    def ensure_runtime_dirs(self) -> None:
        """Ensure runtime directories exist before examples execute."""
        self.outputs.mkdir(parents=True, exist_ok=True)
        self.samples_expected_outputs.mkdir(parents=True, exist_ok=True)


def get_project_paths() -> ProjectPaths:
    """Resolve canonical project paths rooted at repository base."""
    root = Path(__file__).resolve().parents[2]
    paths = ProjectPaths(
        root=root,
        src=root / "src",
        examples=root / "examples",
        docs=root / "docs",
        outputs=root / "outputs",
        samples_expected_outputs=root / "samples" / "expected_outputs",
        data=root / "data",
    )
    paths.ensure_runtime_dirs()
    return paths
