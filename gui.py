import tkinter as tk

from evaluator import evaluate
from history import History
from formatter import format_result
from storage import load_json, save_json

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
        self.settings = load_json("settings.json", {})
        saved_theme = self.settings.get("theme") if isinstance(self.settings, dict) else None
        self.theme_name = saved_theme if saved_theme in THEMES else "dark"
        self.colors = THEMES[self.theme_name]
        self.buttons = []
        self.history = History("history.json")
        self.just_calculated = False
        self.has_error = False
        self.history_visible = False
        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")

        self.create_button("◐", 0, 0, command=self.toggle_theme, kind="icon")          # 69
        self.create_button("☰", 0, 3, command=self.toggle_history, kind="icon")       # YENİ satır

        self.result_label = tk.Label(root, textvariable=self.result_var,
                                     font=("Segoe UI", 12), anchor="e")
        self.result_label.grid(row=0, column=1, columnspan=2, sticky="ew", padx=12, pady=(12, 0))
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
        self.entry.bind("<Control-h>", self.on_history_shortcut)        
        self.create_history_panel()
        self.apply_theme()

    def create_button(self, text, row, column, command=None, kind=None, parent=None):
        kind = kind or get_button_kind(text)
        if command is None:
            command = lambda: self.on_button_click(text)
        span = 3 if text == "=" else 1

        button = tk.Button(parent or self.root, text=text, font=("Segoe UI", 16), width=4,
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
        self.history_frame.config(bg=background)
        self.history_list.config(bg=background, fg=self.colors["text"],
                                 selectbackground=self.colors["operator_hover"],
                                 selectforeground=self.colors["text"])        

    def toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.colors = THEMES[self.theme_name]
        save_json("settings.json", {"theme": self.theme_name})
        self.apply_theme()
        self.entry.focus()

    def create_history_panel(self):
        self.history_frame = tk.Frame(self.root)
        self.history_frame.grid(row=0, column=4, rowspan=len(BUTTONS) + 2,
                                sticky="nsew", padx=(8, 0))
        self.history_frame.grid_rowconfigure(0, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        self.history_list = tk.Listbox(self.history_frame, font=("Segoe UI", 11), width=24,
                                       relief="flat", bd=0, highlightthickness=0,
                                       activestyle="none")
        self.history_list.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.history_list.bind("<<ListboxSelect>>", self.on_history_select)

        self.create_button("Temizle", 1, 0, command=self.clear_history, kind="operator",
                           parent=self.history_frame)
        self.history_frame.grid_remove()
        self.refresh_history()

    def refresh_history(self):
        self.history_entries = list(reversed(self.history.get_all()))
        self.history_list.delete(0, tk.END)
        if not self.history_entries:
            self.history_list.insert(tk.END, "Henüz geçmiş yok")
        for expression, result in self.history_entries:
            self.history_list.insert(tk.END, f"{expression} = {result}")

    def toggle_history(self):
        self.root.update_idletasks()
        width, height = self.root.winfo_width(), self.root.winfo_height()
        panel_width = self.history_frame.winfo_reqwidth() + 8
        if self.history_visible:
            self.history_frame.grid_remove()
            self.root.geometry(f"{width - panel_width}x{height}")
        else:
            self.history_frame.grid()
            self.root.geometry(f"{width + panel_width}x{height}")
        self.history_visible = not self.history_visible
        self.entry.focus()

    def on_history_shortcut(self, event):
        self.toggle_history()
        return "break"

    def on_history_select(self, event):
        selection = self.history_list.curselection()
        if not selection or not self.history_entries:
            return
        expression, result = self.history_entries[selection[0]]
        self.has_error = False
        self.result_var.set(f"{expression} =")
        self.set_expression(result)
        self.just_calculated = True

    def clear_history(self):
        self.history.clear()
        self.refresh_history()
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
        self.refresh_history()
        self.result_var.set(f"{expression} =")
        self.set_expression(result)
        self.just_calculated = True


if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()