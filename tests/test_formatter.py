import unittest

from formatter import format_result


class TestFormatResult(unittest.TestCase):
    def test_formatting(self):
        cases = [
            (14.0, "14"),
            (-2.5, "-2.5"),
            (0.1 + 0.2, "0.3"),
            (1234567.0, "1,234,567"),
            (1e25, "1e+25"),
            (0.1 ** 12, "1e-12"),
            (-0.0, "0"),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(format_result(value), expected)
