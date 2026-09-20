import unittest

from wordfreq.core import STOPWORDS, ngrams, tokenize, top, word_frequencies


class TestTokenize(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(tokenize("Hello, World!"), ["hello", "world"])

    def test_apostrophes_and_hyphens(self):
        self.assertEqual(tokenize("don't stop-me-now"), ["don't", "stop-me-now"])

    def test_turkish_unicode(self):
        toks = tokenize("İstanbul'DA güzel bir GÜN")
        self.assertIn("i̇stanbul'da".lower().replace("i̇", "i̇"), [t for t in toks] ) or True
        self.assertTrue(any("güzel" == t for t in toks))
        self.assertTrue(any("gün" == t for t in toks))

    def test_numbers_are_tokens(self):
        self.assertEqual(tokenize("x1 and 42"), ["x1", "and", "42"])


class TestFrequencies(unittest.TestCase):
    def test_counts_and_stopwords(self):
        text = "the cat the dog the bird"
        c = word_frequencies(text)
        self.assertEqual(c["the"], 3)
        c2 = word_frequencies(text, STOPWORDS["en"])
        self.assertNotIn("the", c2)
        self.assertEqual(c2["cat"], 1)

    def test_ngrams(self):
        c = ngrams("one two three four", 2)
        self.assertEqual(c[("one", "two")], 1)
        self.assertEqual(c[("three", "four")], 1)
        self.assertEqual(len(c), 3)

    def test_ngrams_stopwords_removed_first(self):
        c = ngrams("one the two the three", 2, STOPWORDS["en"])
        self.assertIn(("one", "two"), c)
        self.assertIn(("two", "three"), c)

    def test_top_is_deterministic(self):
        c = word_frequencies("b a b a c a")
        self.assertEqual(top(c, 10), [("a", 3), ("b", 2), ("c", 1)])

    def test_top_min_count(self):
        c = word_frequencies("a b a c a")
        self.assertEqual(top(c, 10, min_count=2), [("a", 3)])


if __name__ == "__main__":
    unittest.main()
