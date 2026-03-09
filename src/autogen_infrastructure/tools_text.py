from __future__ import annotations

import re
from collections import Counter


def word_count(text: str) -> str:
    tokens = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    return str(len(tokens))


def keyword_hits(text: str, keywords_csv: str) -> str:
    keywords = [k.strip() for k in keywords_csv.split(",") if k.strip()]
    lowered = text.lower()
    counts = {k: lowered.count(k.lower()) for k in keywords}
    sorted_items = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return "\n".join(f"{k}: {v}" for k, v in sorted_items)


def top_terms(text: str, top_n: int = 10) -> str:
    tokens = re.findall(r"\b[a-zA-ZÀ-ÿ]{3,}\b", text.lower())
    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "from",
        "you",
        "your",
        "para",
        "com",
        "uma",
        "que",
        "de",
        "do",
        "da",
        "dos",
        "das",
        "em",
    }
    filtered = [t for t in tokens if t not in stopwords]
    counter = Counter(filtered)
    return "\n".join(f"{term}: {count}" for term, count in counter.most_common(top_n))
