import math

from tokenizer import tokenize

TRIG_FUNCTIONS = ("sin", "cos", "tan")
CONSTANTS = {
    "π": math.pi,
    "pi": math.pi,
    "e": math.e,
}


def square_root(x):
    if x < 0:
        raise ValueError("Negatif sayının karekökü alınamaz")
    return math.sqrt(x)


def logarithm(x):
    if x <= 0:
        raise ValueError("Logaritma sadece pozitif sayılar için tanımlıdır")
    return math.log10(x)


def natural_log(x):
    if x <= 0:
        raise ValueError("Logaritma sadece pozitif sayılar için tanımlıdır")
    return math.log(x)


FUNCTIONS = {
    "sqrt": square_root,
    "log": logarithm,
    "ln": natural_log,
    "abs": abs,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
}


class Parser:
    def __init__(self, tokens, degrees=False):
        self.tokens = tokens
        self.pos = 0
        self.degrees = degrees

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    def expect(self, expected):
        token = self.advance()
        if token != expected:
            raise ValueError(f"'{expected}' bekleniyordu")
        
    def parse_expression(self):
        result = self.parse_term()
        while self.peek() in ("+", "-"):
            operator = self.advance()
            right = self.parse_term()
            if operator == "+":
                result += right
            else:
                result -= right
        return result

    def is_implicit_multiplication(self):
        token = self.peek()
        return token == "(" or (isinstance(token, str) and token.isalpha())

    def parse_term(self):
        result = self.parse_unary()
        while self.peek() in ("*", "/") or self.is_implicit_multiplication():
            if self.is_implicit_multiplication():
                operator = "*"
            else:
                operator = self.advance()

            right = self.parse_unary()
            if operator == "*":
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Sıfıra bölme yapılamaz")
                result /= right
        return result

    def parse_unary(self):
        if self.peek() == "-":
            self.advance()
            return -self.parse_unary()
        if self.peek() == "+":
            self.advance()
            return self.parse_unary()
        return self.parse_power()

    def parse_power(self):
        base = self.parse_primary()
        if self.peek() == "^":
            self.advance()
            exponent = self.parse_unary()
            if base == 0 and exponent < 0:
                raise ZeroDivisionError("Sıfıra bölme yapılamaz")
            if base < 0 and exponent != int(exponent):
                raise ValueError("Negatif sayının ondalıklı kuvveti alınamaz")
            try:
                return base ** exponent
            except OverflowError:
                raise OverflowError("Sonuç çok büyük")
        return base


    def parse_primary(self):
        token = self.advance()

        if isinstance(token, float):
            return token

        if token == "(":
            value = self.parse_expression()
            self.expect(")")
            return value


        if token in FUNCTIONS:
            self.expect("(")
            argument = self.parse_expression()
            self.expect(")")
            if token in TRIG_FUNCTIONS:
                return self.apply_trig(token, argument)
            return FUNCTIONS[token](argument)

        if token in CONSTANTS:
            return CONSTANTS[token]

        if token is None:
            raise ValueError("İfade eksik")
        raise ValueError(f"Beklenmeyen ifade: '{token}'")

    def apply_trig(self, name, argument):
        if self.degrees:
            argument = math.radians(argument)
        if name == "tan" and abs(math.cos(argument)) < 1e-12:
            raise ValueError("Bu açının tanjantı tanımsız")
        result = FUNCTIONS[name](argument)
        return 0.0 if abs(result) < 1e-12 else result

def evaluate(expression, degrees=False):
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Boş ifade")
    parser = Parser(tokens, degrees)
    result = parser.parse_expression()
    if parser.peek() is not None:
        raise ValueError(f"Beklenmeyen ifade: '{parser.peek()}'")

    if math.isinf(result):
        raise OverflowError("Sonuç çok büyük")

    return result