"""wordfreq — word frequency and n-gram analyzer, zero dependencies."""

from .core import ngrams, tokenize, top, word_frequencies

__version__ = "1.0.0"
__all__ = ["tokenize", "word_frequencies", "ngrams", "top", "__version__"]
