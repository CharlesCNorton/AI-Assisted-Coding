import tkinter as tk
import math
import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.Pow: operator.pow
}

ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,
    ast.Name
}

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, _=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, background="#ffffff")
        label.pack()

    def hide_tooltip(self, _=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class Calculator:
    def __init__(self):
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'g': 9.81,
            'c': 299792458,
            'h': 6.62607015e-34
        }
        self.functions = {
            'sqrt': math.sqrt,
            'log': math.log,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp
        }

    def eval_expr(self, expr):
        expr = expr.replace('^', '**')
        for func in self.functions:
            expr = expr.replace(func, f"math.{func}")
        for const in self.constants:
            expr = expr.replace(const, str(self.constants[const]))
        return self._eval(ast.parse(expr, mode='eval').body)

    def _eval(self, node):
        if type(node) not in ALLOWED_NODES:
            raise TypeError(f"Unsupported type: {type(node)}")
        
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return OPERATORS[type(node.op)](self._eval(node.left), self._eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return OPERATORS[type(node.op)](self._eval(node.operand))
        else:
            raise TypeError(node)

class CalculatorGUI:
    def __init__(self, calculator):
        self.calculator = calculator
        self.window = tk.Tk()
        self.window.title('Calculator')
        self.entry = tk.Entry(self.window, width=35, font=('Arial', 14))
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
        self.entry.bind('<Return>', self.equals)
        self.entry.bind('<Escape>', self.clear)
        self.entry.focus_set()  # Set focus on the Entry widget
        
        buttons = [
            ['7', '8', '9', '/', 'sqrt', '(', ')'],
            ['4', '5', '6', '*', 'log', 'pi', 'e'],
            ['1', '2', '3', '-', 'sin', '^', 'c'],
            ['0', '.', '=', '+', 'cos', 'h', 'g'],
            ['Clear', '', '', '', 'tan', 'exp', '']
        ]

        tooltips = {
            'pi': 'Pi - Mathematical constant',
            'e': "Euler's number",
            'g': 'Acceleration due to gravity',
            'c': 'Speed of light',
            'h': "Planck's constant",
            'sqrt': 'Square root',
            'log': 'Natural logarithm',
            'sin': 'Sine function',
            'cos': 'Cosine function',
            'tan': 'Tangent function',
            'exp': 'Exponential function'
        }

        for i, row in enumerate(buttons):
            self.create_buttons(i, row, tooltips)

    def create_buttons(self, i, row, tooltips):
        for j, button in enumerate(row):
            if button:
                btn = tk.Button(self.window, text=button, width=5, height=2, font=('Arial', 12),
                                command=lambda x=button: self.handle_button_click(x))
                btn.grid(row=i+1, column=j, padx=5, pady=5)
                if button in tooltips:
                    ToolTip(btn, tooltips[button])

    def handle_button_click(self, button):
        self.entry.focus_set()  # Set focus back to Entry widget
        if button == '=':
            self.equals(None)
        elif button == 'Clear':
            self.clear(None)
        else:
            current_expression = self.entry.get()
            self.entry.delete(0, 'end')
            self.entry.insert('end', current_expression + button)

    def equals(self, event):
        expression = self.entry.get().strip()
        if not expression:
            self.show_error('Empty input')
        else:
            try:
                result = str(self.calculator.eval_expr(expression))
                self.entry.delete(0, 'end')
                self.entry.insert('end', result)
            except Exception as e:
                self.show_error(str(e))

    def clear(self, event):
        self.entry.delete(0, 'end')

    def show_error(self, message):
        self.entry.delete(0, 'end')
        self.entry.insert('end', f'Error: {message}')

    def run(self):
        self.window.mainloop()

def main():
    calc = Calculator()
    gui = CalculatorGUI(calc)
    gui.run()

if __name__ == "__main__":
    main()