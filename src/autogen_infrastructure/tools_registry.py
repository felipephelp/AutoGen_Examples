from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .tools_data import csv_head
from .tools_fs import list_directory, list_text_files, read_text_file
from .tools_text import keyword_hits, top_terms, word_count


def file_explorer_tools() -> list[Callable[..., Any]]:
    """Return filesystem-oriented tool set."""
    return [list_directory, list_text_files, read_text_file]


def text_analysis_tools() -> list[Callable[..., Any]]:
    """Return text-analysis tool set."""
    return [read_text_file, word_count, keyword_hits, top_terms]


def data_tools() -> list[Callable[..., Any]]:
    """Return structured-data tool set."""
    return [csv_head]
