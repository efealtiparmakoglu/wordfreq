"""wordfreq: word frequency and n-gram analyzer.

Tokenization is Unicode-aware (words are runs of letters/digits including
internal apostrophes and hyphens), lowercased for counting. Stopword lists
for English and Turkish are built in.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

TOKEN_RE = re.compile(r"[\w]+(?:['’\-][\w]+)*", re.UNICODE)

STOPWORDS: dict[str, set[str]] = {
    "en": {
        "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
        "has", "have", "he", "her", "his", "i", "in", "is", "it", "its", "of",
        "on", "or", "she", "that", "the", "their", "they", "this", "to", "was",
        "were", "will", "with", "you", "your", "not", "no", "we", "us", "our",
        "do", "does", "did", "so", "if", "then", "than", "there", "here",
    },
    "tr": {
        "bir", "ve", "bu", "şu", "o", "ile", "için", "gibi", "daha", "çok",
        "ama", "fakat", "yani", "de", "da", "ki", "mi", "mı", "ise", "her",
        "hem", "ya", "veya", "olarak", "olan", "olan", "ben", "sen", "biz",
        "siz", "onlar", "ne", "nasıl", "neden", "var", "yok", "ise",
    },
}


def tokenize(text: str) -> list[str]:
    """Lowercased word tokens; NFKD-normalized so accented forms are stable."""
    text = unicodedata.normalize("NFC", text)
    return [m.group(0).lower() for m in TOKEN_RE.finditer(text)]


def word_frequencies(text: str, stopwords: set[str] | None = None) -> Counter:
    counter = Counter(tokenize(text))
    if stopwords:
        for sw in stopwords:
            counter.pop(sw, None)
    return counter


def ngrams(text: str, n: int, stopwords: set[str] | None = None) -> Counter:
    """Word n-grams; n>=2 sequences skip any n-gram containing a stopword."""
    if n < 1:
        raise ValueError("n must be >= 1")
    tokens = tokenize(text)
    if stopwords:
        tokens = [t for t in tokens if t not in stopwords]
    return Counter(tuple(tokens[i: i + n]) for i in range(len(tokens) - n + 1))


def top(counter: Counter, limit: int, min_count: int = 1) -> list[tuple]:
    """Top entries sorted by count desc, then key asc (deterministic)."""
    return sorted(
        ((k, c) for k, c in counter.items() if c >= min_count),
        key=lambda kv: (-kv[1], kv[0]),
    )[: max(0, limit)]
