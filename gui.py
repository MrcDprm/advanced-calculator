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

CONTINUE_OPERATORS = "+-*/^"
ALLOWED_CHARS = "0123456789.,+-*/^() "
EDIT_KEYS = ("BackSpace", "Delete", "Left", "Right", "Home", "End")


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş Hesap Makinesi")
        self.root.resizable(False, False)
        self.history = History()
        self.just_calculated = False
        self.has_error = False

        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")

        self.entry = tk.Entry(root, textvariable=self.expression_var,
                              font=("Consolas", 18), justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, sticky="ew", padx=8, pady=(8, 0))
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
        self.entry.bind("<Key>", self.on_key)
        self.entry.bind("<Button-1>", self.on_entry_click)

    def on_button_click(self, value):
        if value == "C":
            self.clear()
        elif value == "⌫":
            self.just_calculated = False
            self.backspace()
        elif value == "=":
            self.calculate()
        elif value == "√":
            self.prepare_for_input("sqrt(")
            self.insert_text("sqrt(")
        else:
            self.prepare_for_input(value)
            self.insert_text(value)


    def set_expression(self, text):
        self.expression_var.set(text)
        self.entry.icursor(tk.END)
        self.entry.xview_moveto(1)
        self.entry.focus()

    def insert_text(self, text):
        if self.entry.selection_present():
            self.entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.entry.insert(tk.INSERT, text)
        self.entry.focus()

    def backspace(self):
        if self.entry.selection_present():
            self.entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            position = self.entry.index(tk.INSERT)
            if position > 0:
                self.entry.delete(position - 1)
        self.entry.focus()

    def clear_error(self):
        if self.has_error:
            self.result_var.set("")
            self.has_error = False

    def prepare_for_input(self, text):
        self.clear_error()
        if self.just_calculated:
            self.just_calculated = False
            if text[0] not in CONTINUE_OPERATORS:
                self.set_expression("")
                self.result_var.set("")

    def on_key(self, event):
        if event.char == "=":
            self.calculate()
            return "break"
        if event.char and event.char.isprintable():
            if event.char not in ALLOWED_CHARS and not event.char.isalpha():
                return "break"
            self.prepare_for_input(event.char)
        elif event.keysym in EDIT_KEYS:
            self.just_calculated = False
            self.clear_error()

    def on_entry_click(self, event):
        self.just_calculated = False

    def clear(self):
        self.set_expression("")
        self.result_var.set("0")
        self.just_calculated = False
        self.has_error = False        

    def calculate(self):
        expression = self.expression_var.get().strip()
        if not expression:
            return
        try:
            result = format_result(evaluate(expression))
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            self.result_var.set(f"Hata: {error}")
            self.has_error = True
            return
        self.history.add(expression, result)
        self.result_var.set(f"{expression} =")
        self.set_expression(result)
        self.just_calculated = True
        


if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()