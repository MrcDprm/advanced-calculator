import re

OPERATORS = "+-*/^()!%"
GROUPED_NUMBER = re.compile(r"\d{1,3}(,\d{3})+(\.\d*)?([eE][+-]?\d+)?")


def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
        elif char in OPERATORS:
            tokens.append(char)
            i += 1
        elif char.isdigit() or char == ".":
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] in ".,"):
                i += 1
            if i < len(expression) and expression[i] in "eE":
                j = i + 1
                if j < len(expression) and expression[j] in "+-":
                    j += 1
                if j < len(expression) and expression[j].isdigit():
                    i = j
                    while i < len(expression) and expression[i].isdigit():
                        i += 1
            raw_text = expression[start:i]
            if "," in raw_text and not GROUPED_NUMBER.fullmatch(raw_text):
                raise ValueError(f"Geçersiz sayı: '{raw_text}' (ondalık için nokta kullanın)")
            number_text = raw_text.replace(",", "")
            try:
                tokens.append(float(number_text))
            except ValueError:
                raise ValueError(f"Geçersiz sayı: '{number_text}'")
        elif char.isalpha():
            start = i
            while i < len(expression) and expression[i].isalpha():
                i += 1
            tokens.append(expression[start:i])
        else:
            raise ValueError(f"Geçersiz karakter: '{char}'")

    return tokens
