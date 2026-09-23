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
EDIT_KEYS = ("Left", "Right", "Home", "End")
KEY_SHORTCUTS = {
    "@": "sqrt(",
}
FUNCTION_TOKENS = ("sqrt(",)


THEMES = {
    "dark": {
        "background": "#202020", "text": "#ffffff", "muted": "#9d9d9d",
        "digit": "#3b3b3b", "digit_hover": "#454545",
        "operator": "#2d2d2d", "operator_hover": "#383838",
        "equals": "#4cc2ff", "equals_hover": "#48b2e9", "equals_text": "#000000",
        "icon": "#202020", "icon_hover": "#2d2d2d",        
    },
    "light": {
        "background": "#f3f3f3", "text": "#000000", "muted": "#606060",
        "digit": "#ffffff", "digit_hover": "#f0f0f0",
        "operator": "#e9e9e9", "operator_hover": "#dcdcdc",
        "equals": "#005fb8", "equals_hover": "#196ebf", "equals_text": "#ffffff",
        "icon": "#f3f3f3", "icon_hover": "#e9e9e9",
    },
}


def get_button_kind(text):
    if text.isdigit() or text == ".":
        return "digit"
    if text == "=":
        return "equals"
    return "operator"


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş Hesap Makinesi")
        self.root.minsize(320, 460)
        self.theme_name = "dark"
        self.colors = THEMES[self.theme_name]
        self.buttons = []
        self.history = History()
        self.just_calculated = False
        self.has_error = False

        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")

        self.create_button("◐", 0, 0, command=self.toggle_theme, kind="icon")

        self.result_label = tk.Label(root, textvariable=self.result_var,
                                     font=("Segoe UI", 12), anchor="e")
        self.result_label.grid(row=0, column=1, columnspan=3, sticky="ew", padx=12, pady=(12, 0))
        self.result_label.bind("<Configure>",
                               lambda event: self.result_label.config(wraplength=event.width))

        self.entry = tk.Entry(root, textvariable=self.expression_var, font=("Segoe UI", 28),
                              justify="right", relief="flat", bd=0)
        self.entry.grid(row=1, column=0, columnspan=4, sticky="ew", padx=12, pady=(0, 12))
        self.entry.focus()

        for row_index, row in enumerate(BUTTONS):
            for column_index, text in enumerate(row):
                self.create_button(text, row_index + 2, column_index)

        for column in range(4):
            root.grid_columnconfigure(column, weight=1, uniform="button")
        for row in range(len(BUTTONS)):
            root.grid_rowconfigure(row + 2, weight=1, uniform="button")

        root.bind("<Return>", lambda event: self.calculate())
        root.bind("<Escape>", lambda event: self.clear())
        self.entry.bind("<Key>", self.on_key)
        self.entry.bind("<Button-1>", self.on_entry_click)
        self.entry.bind("<<Copy>>", self.on_copy)
        self.entry.bind("<<Paste>>", self.on_paste)

        self.apply_theme()

    def create_button(self, text, row, column, command=None, kind=None):
        kind = kind or get_button_kind(text)
        if command is None:
            command = lambda: self.on_button_click(text)
        span = 3 if text == "=" else 1

        button = tk.Button(self.root, text=text, font=("Segoe UI", 16), width=4,
                           relief="flat", bd=0, cursor="hand2", command=command)
        button.grid(row=row, column=column, columnspan=span, sticky="nsew", padx=1, pady=1)
        button.bind("<Enter>", lambda event: self.paint_button(button, kind, hover=True))
        button.bind("<Leave>", lambda event: self.paint_button(button, kind, hover=False))
        self.buttons.append((button, kind))

    def paint_button(self, button, kind, hover):
        key = f"{kind}_hover" if hover else kind
        text_color = self.colors["equals_text"] if kind == "equals" else self.colors["text"]
        button.config(bg=self.colors[key], fg=text_color,
                      activebackground=self.colors[f"{kind}_hover"],
                      activeforeground=text_color)

    def apply_theme(self):
        background = self.colors["background"]
        self.root.configure(bg=background)
        self.result_label.config(bg=background, fg=self.colors["muted"])
        self.entry.config(bg=background, fg=self.colors["text"],
                          insertbackground=self.colors["text"])
        for button, kind in self.buttons:
            self.paint_button(button, kind, hover=False)

    def toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.colors = THEMES[self.theme_name]
        self.apply_theme()
        self.entry.focus()

    def on_button_click(self, value):
        if value == "C":
            self.clear()
        elif value == "⌫":
            self.just_calculated = False
            self.delete_char(forward=False)
        elif value == "=":
            self.calculate()
        elif value == "√":
            self.type_text("sqrt(")
        else:
            self.type_text(value)

    def set_expression(self, text):
        self.expression_var.set(text)
        self.entry.icursor(tk.END)
        self.entry.xview_moveto(1)
        self.entry.focus()

    def type_text(self, text):
        self.prepare_for_input(text)
        self.insert_text(text)

    def insert_text(self, text):
        if self.entry.selection_present():
            self.entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.entry.insert(tk.INSERT, text)
        self.entry.focus()

    def find_function_span(self, position, forward):
        text = self.expression_var.get()
        for token in FUNCTION_TOKENS:
            start = text.find(token)
            while start != -1:
                end = start + len(token)
                if forward and start <= position < end:
                    return start, end
                if not forward and start < position <= end:
                    return start, end
                start = text.find(token, start + 1)
        return None

    def delete_char(self, forward):
        if self.entry.selection_present():
            self.entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            position = self.entry.index(tk.INSERT)
            span = self.find_function_span(position, forward)
            if span:
                start, end = span
                self.entry.delete(start, end)
            elif forward:
                self.entry.delete(position)
            elif position > 0:
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
        if event.keysym in ("BackSpace", "Delete"):
            self.just_calculated = False
            self.clear_error()
            self.delete_char(forward=event.keysym == "Delete")
            return "break"
        if event.char in KEY_SHORTCUTS:
            self.type_text(KEY_SHORTCUTS[event.char])
            return "break"
        if event.char and event.char.isprintable():
            if event.char not in ALLOWED_CHARS:
                return "break"
            self.prepare_for_input(event.char)
        elif event.keysym in EDIT_KEYS:
            self.just_calculated = False
            self.clear_error()

    def on_entry_click(self, event):
        self.just_calculated = False

    def on_copy(self, event):
        if self.entry.selection_present():
            return None
        self.root.clipboard_clear()
        self.root.clipboard_append(self.expression_var.get())
        return "break"

    def on_paste(self, event):
        try:
            text = self.root.clipboard_get().strip()
        except tk.TclError:
            return "break"
        check = text
        for token in FUNCTION_TOKENS:
            check = check.replace(token, "")
        if all(char in ALLOWED_CHARS for char in check):
            self.type_text(text)
        else:
            self.result_var.set("Hata: Yapıştırılan metin geçersiz")
            self.has_error = True
        return "break"

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