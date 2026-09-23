OPERATORS = "+-*/^()"


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
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            number_text = expression[start:i]
            try:
                tokens.append(float(number_text))
            except ValueError:
                raise ValueError(f"Geçersiz Sayı: '{number_text}'")
        elif char.isalpha():
            start = i
            while i < len(expression) and expression[i].isalpha():
                i += 1
            tokens.append(expression[start:i])
        else:
            raise ValueError(f"Geçersiz Karakter: '{char}'")

    return tokens