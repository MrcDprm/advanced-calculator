import tkinter as tk
from evaluator import evaluate
from history import History
from formatter import format_result


BUTTONS = [
    ["C", "⌫", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["√", "0", ".", "+"],
    ["^", "="],
]



class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş Hesap Makinesi")
        self.root.resizable(False, False)
        self.history = History()

        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")

        self.entry = tk.Entry(root, textvariable=self.expression_var,
                         font=("Consolas", 18), justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, sticky="ew", padx=8, pady=(8,0))
        self.entry.focus()

        result_label = tk.Label(root, textvariable=self.result_var,
                                font=("Consolas", 14), anchor="e", fg="gray",
                                wraplength=300)
        result_label.grid(row=1, column=0, columnspan=4, sticky="ew", padx=8, pady=(0, 8))


        for row_index, row in enumerate(BUTTONS):
            for column_index, text in enumerate(row):
                span = 3 if text == "=" else 1
                button = tk.Button(root, text=text, font=("Consolas", 16), width=4,
                                   command=lambda value=text: self.on_button_click(value))
                button.grid(row=row_index + 2, column=column_index, columnspan=span,
                            sticky="nsew", padx=2, pady=2)

        root.bind("<Return>", lambda event: self.calculate())
        root.bind("<Escape>", lambda event: self.clear())

    def on_button_click(self, value):
        if value == "C":
            self.clear()
        elif value == "⌫":
            self.set_expression(self.expression_var.get()[:-1])
        elif value == "=":
            self.calculate()
        elif value == "√":
            self.set_expression(self.expression_var.get() + "sqrt(")
        else:
            self.set_expression(self.expression_var.get() + value)


    def set_expression(self, text):
        self.expression_var.set(text)
        self.entry.icursor(tk.END)
        self.entry.xview_moveto(1)
        self.entry.focus()

    def clear(self):
        self.set_expression("")
        self.result_var.set("0")

    def calculate(self):
        expression = self.expression_var.get().strip()
        if not expression:
            return
        try:
            result = format_result(evaluate(expression))
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            self.result_var.set(f"Hata: {error}")
            return
        self.history.add(expression, result)
        self.result_var.set(f"{expression} =")
        self.set_expression(result)
        


if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()