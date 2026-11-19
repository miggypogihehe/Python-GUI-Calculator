import tkinter as tk
import ast
import operator


window = tk.Tk()
window.title("Calculator")
window.geometry("350x500")
window.resizable(False, False)
window.configure(bg="#edf4f7")

expression = ""


display = tk.Entry(
    window,
    font=("Arial", 24),
    bg="light blue",
    fg="white",
    insertbackground="white",
    justify="right",
    bd=0
)
display.pack(fill="x", padx=15, pady=20, ipady=20)


def sync_expression(event=None):
    global expression
    expression = display.get()


def validate_input(event):
    allowed = "0123456789.+-*/()"
    if event.char in allowed or event.keysym in (
        "BackSpace", "Delete", "Left", "Right", "Home", "End"
    ):
        return None
    return "break"

display.bind("<Key>", validate_input)
display.bind("<KeyRelease>", sync_expression)


def button_click(value):
    global expression
    expression += str(value)
    display.delete(0, tk.END)
    display.insert(tk.END, expression)


def clear():
    global expression
    expression = ""
    display.delete(0, tk.END)


def backspace():
    global expression
    expression = expression[:-1]
    display.delete(0, tk.END)
    display.insert(tk.END, expression)


def safe_calculate(node):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg
    }

    if isinstance(node, ast.Expression):
        return safe_calculate(node.body)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in operations:
        left = safe_calculate(node.left)
        right = safe_calculate(node.right)
        return operations[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
        return operations[type(node.op)](safe_calculate(node.operand))

    raise ValueError("Invalid expression")

def calculate():
    global expression
    try:
        if not expression.strip():
            return
        result = safe_calculate(ast.parse(expression, mode="eval"))
        display.delete(0, tk.END)
        display.insert(tk.END, str(result))
        expression = str(result)
    except (ValueError, SyntaxError, ZeroDivisionError, TypeError):
        display.delete(0, tk.END)
        display.insert(tk.END, "ERROR")
        expression = ""


buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]


button_frame = tk.Frame(window, bg="#94dbfc")
button_frame.pack(expand=True, fill="both", padx=10, pady=5)


clear_button = tk.Button(
    button_frame,
    text="C",
    font=("Arial", 18, "bold"),
    bg="#067a8a",
    fg="white",
    bd=0,
    command=clear
)
clear_button.grid(
    row=0, column=0, columnspan=2,
    sticky="nsew", padx=4, pady=4
)

backspace_button = tk.Button(
    button_frame,
    text="⌫",
    font=("Arial", 18, "bold"),
    bg="#173541",
    fg="white",
    bd=0,
    command=backspace
)
backspace_button.grid(
    row=0, column=2, columnspan=2,
    sticky="nsew", padx=4, pady=4
)


for row_index, row in enumerate(buttons, start=1):
    for col_index, value in enumerate(row):
        if value == "=":
            command = calculate
            color = "#5f0cbe"
        elif value in ["+", "-", "*", "/"]:
            command = lambda v=value: button_click(v)
            color = "#160441"
        else:
            command = lambda v=value: button_click(v)
            color = "#a99eda"

        button = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 18, "bold"),
            bg=color,
            fg="white",
            bd=0,
            command=command
        )
        button.grid(
            row=row_index,
            column=col_index,
            sticky="nsew",
            padx=4,
            pady=4
        )


for i in range(5):
    button_frame.grid_rowconfigure(i, weight=1)

for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)


window.mainloop()
