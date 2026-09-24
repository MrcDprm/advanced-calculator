import unittest

from evaluator import evaluate


class TestEvaluate(unittest.TestCase):
    def test_valid_expressions(self):
        cases = [
            ("2 + 3 * 4", 14),
            ("(2 + 3) * 4", 20),
            ("10 - 3 - 2", 5),
            ("-2 ^ 2", -4),
            ("2 ^ 3 ^ 2", 512),
            ("2(3)", 6),
            ("(1+2)(3+4)", 21),
            ("sqrt(16) + 2 ^ 3", 12),
            ("5!", 120),
            ("200+10%", 220),
            ("200-10%", 180),
            ("50*10%", 5),
            ("log(1000)", 3),
            ("abs(-7.5)", 7.5),
            ("1,000 + 1", 1001),
            ("1e3", 1000),
            ("1,234.5 + 0.5", 1235),
            ("((0.1+0.2)*10)!", 6),
        ]
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.assertAlmostEqual(evaluate(expression), expected)

    def test_trigonometry_in_degrees(self):
        self.assertAlmostEqual(evaluate("sin(30)", degrees=True), 0.5)
        self.assertEqual(evaluate("cos(90)", degrees=True), 0)
        self.assertAlmostEqual(evaluate("tan(45)", degrees=True), 1)

    def test_trigonometry_in_radians(self):
        self.assertAlmostEqual(evaluate("sin(pi/2)"), 1)
        self.assertEqual(evaluate("sin(pi)"), 0)

    def test_errors(self):
        cases = [
            ("10 / 0", ZeroDivisionError),
            ("0 ^ -1", ZeroDivisionError),
            ("(3 + 4", ValueError),
            ("3 4", ValueError),
            ("3 +", ValueError),
            ("", ValueError),
            ("abc(4)", ValueError),
            ("sqrt(-4)", ValueError),
            ("log(0)", ValueError),
            ("(-8) ^ 0.5", ValueError),
            ("2.5!", ValueError),
            ("tan(90)", ValueError),
            ("10 ^ 1000", OverflowError),
            ("171!", OverflowError),
            ("2,5", ValueError),
            ("1,,2", ValueError),
            ("1.234,56", ValueError),
            ("(" * 2000 + "1" + ")" * 2000, ValueError),
            ("-" * 3000 + "5", ValueError),
            ("(10^308*10)-(10^308*10)", OverflowError),
            ("1e999", OverflowError),
            ("sin(1e999)", OverflowError),
        ]
        for expression, error in cases:
            with self.subTest(expression=expression):
                with self.assertRaises(error):
                    evaluate(expression, degrees=True)
