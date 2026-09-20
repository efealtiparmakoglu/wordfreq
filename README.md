# wordfreq

**Word frequency and n-gram analyzer — Unicode-aware tokenization, TR/EN stopwords, zero dependencies.**

[![CI](https://github.com/efealtiparmakoglu/wordfreq/actions/workflows/ci.yml/badge.svg)](https://github.com/efealtiparmakoglu/wordfreq/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org)

```
$ wordfreq article.txt --stopwords en -t 5
  freq  term
--------------
     3  python
     2  again
     1  brown
```

Counts word frequencies across any text, builds word n-grams, filters
stopwords, and prints deterministic top-N lists in three formats. Tokenize
is Unicode-aware: apostrophes ("don't"), hyphens ("stop-me-now") and
accented letters survive intact.

## Usage

```sh
wordfreq text.txt --stopwords en -t 25          # top 25, EN stopwords out
wordfreq gunluk.txt --stopwords tr -n 2 -t 10   # Turkish 2-grams
cat *.txt | wordfreq --all -f json              # whole stream as JSON
wordfreq text.txt --extra-stopwords my-list.txt
```

| Option | Meaning |
|---|---|
| `-n, --ngram N` | n-gram size (default 1) |
| `-t, --top N` | show top N (default 25) |
| `-m, --min-count N` | minimum count filter |
| `--stopwords none\|en\|tr` | built-in stopword lists |
| `--extra-stopwords FILE` | one stopword per line, added on top |
| `-f, --format` | table, tsv or json |

Deterministic ordering: count descending, term ascending.

## Development

```sh
python3 -m unittest discover -s tests
```

## License

MIT — see [LICENSE](LICENSE).
