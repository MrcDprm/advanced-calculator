import unittest

from tokenizer import tokenize


class TestTokenize(unittest.TestCase):
    def test_numbers_and_operators(self):
        self.assertEqual(tokenize("(3 + 45) * 2.5"), ["(", 3.0, "+", 45.0, ")", "*", 2.5])

    def test_function_names(self):
        self.assertEqual(tokenize("sqrt(16)"), ["sqrt", "(", 16.0, ")"])

    def test_thousands_separator(self):
        self.assertEqual(tokenize("1,234"), [1234.0])

    def test_scientific_notation(self):
        self.assertEqual(tokenize("1e+25"), [1e25])
        self.assertEqual(tokenize("2e"), [2.0, "e"])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            tokenize("1.2.3")
        with self.assertRaises(ValueError):
            tokenize("#")
