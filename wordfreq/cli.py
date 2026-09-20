"""Command line entry point for wordfreq."""

import argparse
import json
import sys
from pathlib import Path

from .core import STOPWORDS, ngrams, top, word_frequencies

VERSION = "1.0.0"


def read_inputs(paths: list[str]) -> str:
    chunks = []
    for p in paths:
        try:
            chunks.append(Path(p).read_text(encoding="utf-8", errors="replace"))
        except OSError as e:
            print(f"wordfreq: {p}: {e}", file=sys.stderr)
            sys.exit(1)
    if not paths:
        chunks.append(sys.stdin.read())
    return "\n".join(chunks)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="wordfreq",
        description="Word frequency and n-gram analyzer. Zero dependencies.",
    )
    ap.add_argument("files", nargs="*", help="input text files (default: stdin)")
    ap.add_argument("-n", "--ngram", type=int, default=1, help="n-gram size (default 1)")
    ap.add_argument("-t", "--top", type=int, default=25, help="show top N (default 25)")
    ap.add_argument("-m", "--min-count", type=int, default=1, help="minimum count")
    ap.add_argument("--stopwords", choices=("none", "en", "tr"), default="none")
    ap.add_argument("--extra-stopwords", metavar="FILE",
                    help="file with one stopword per line, added to the list")
    ap.add_argument("-f", "--format", choices=("table", "json", "tsv"), default="table")
    ap.add_argument("--all", action="store_true", help="show everything (no top limit)")
    ap.add_argument("-V", "--version", action="version", version=f"wordfreq {VERSION}")
    args = ap.parse_args(argv)

    text = read_inputs(args.files)
    stopwords: set[str] = set()
    if args.stopwords != "none":
        stopwords |= STOPWORDS[args.stopwords]
    if args.extra_stopwords:
        try:
            content = Path(args.extra_stopwords).read_text(encoding="utf-8")
        except OSError as e:
            print(f"wordfreq: {e}", file=sys.stderr)
            return 1
        stopwords |= {line.strip().lower() for line in content.splitlines() if line.strip()}

    if args.ngram < 1:
        print("wordfreq: --ngram must be >= 1", file=sys.stderr)
        return 2
    counter = ngrams(text, args.ngram, stopwords or None) if args.ngram > 1 else \
        word_frequencies(text, stopwords or None)
    limit = len(counter) if args.all else args.top
    results = top(counter, limit, args.min_count)

    if args.format == "json":
        print(json.dumps([{"n": " ".join(k) if isinstance(k, tuple) else k, "count": c}
                          for k, c in results], ensure_ascii=False, indent=2))
    elif args.format == "tsv":
        for k, c in results:
            key = " ".join(k) if isinstance(k, tuple) else k
            print(f"{c}\t{key}")
    else:
        width = max((len(" ".join(k) if isinstance(k, tuple) else k) for k, _ in results),
                    default=4)
        width = max(width, 4)
        print(f"{'freq':>6}  {'term':<{width}}")
        print("-" * (width + 8))
        for k, c in results:
            key = " ".join(k) if isinstance(k, tuple) else k
            print(f"{c:>6}  {key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
