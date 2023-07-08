import tkinter as tk
import math
import re
import ast
import operator

# Dictionary of supported operators
OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.USub: operator.neg, ast.Pow: operator.pow}

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, background="#ffffff")
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class Calculator:
    def __init__(self):
        self.constants = {
            'pi': 'math.pi',
            'e': 'math.e',
            'g': '9.81',  # acceleration due to gravity
            'c': '299792458',  # speed of light in m/s
            'h': '6.62607015e-34'  # Planck's constant in m^2 kg / s
        }
        self.functions = {
            'sqrt': 'math.sqrt',
            'log': 'math.log',
            'sin': 'math.sin',
            'cos': 'math.cos'
        }
        self.tooltips = {
            'pi': 'Pi is a mathematical constant whose value is the ratio of any circle\'s circumference to its diameter.',
            'e': 'Euler\'s number (e) is the base of the natural logarithm.',
            'g': 'The acceleration due to gravity on Earth.',
            'c': 'The speed of light in vacuum.',
            'h': 'Planck\'s constant, used in quantum mechanics.',
            'sqrt': 'Square root function. sqrt(x) returns the square root of x.',
            'log': 'Natural logarithm function. log(x) returns the natural logarithm of x.',
            'sin': 'Sine function. sin(x) returns the sine of x (x is in radians).',
            'cos': 'Cosine function. cos(x) returns the cosine of x (x is in radians).'
        }

    def eval_expr(self, expr):
        return self._eval(ast.parse(expr, mode='eval').body)

    def _eval(self, node):
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return OPERATORS[type(node.op)](self._eval(node.left), self._eval(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
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
        buttons = [
            ['7', '8', '9', '/', 'sqrt', '(', ')'],
            ['4', '5', '6', '*', 'log', 'pi', 'e'],
            ['1', '2', '3', '-', 'sin', '^', 'c'],
            ['0', '.', '=', '+', 'cos', 'h', 'g'],
            ['Clear', '', '', '', '', '', '']
        ]
        for i, row in enumerate(buttons):
            for j, button in enumerate(row):
                if button != '':
                    if button in self.calculator.constants or button in self.calculator.functions:
                        btn = tk.Button(self.window, text=button, width=5, height=2, font=('Arial', 12), command=lambda x=button: self.handle_button_click(self.calculator.constants.get(x, self.calculator.functions.get(x, x))))
                        ToolTip(btn, self.calculator.tooltips.get(button, ""))
                    else:
                        btn = tk.Button(self.window, text=button, width=5, height=2, font=('Arial', 12), command=lambda x=button: self.handle_button_click(x))
                    btn.grid(row=i+1, column=j, padx=5, pady=5)

    def handle_button_click(self, button):
        if button == '=':
            self.equals()
        elif button == 'Clear':
            self.clear()
        else:
            current_expression = self.entry.get()
            self.entry.delete(0, 'end')
            self.entry.insert('end', current_expression + button)

    def equals(self):
        expression = self.entry.get().strip()
        if expression == '':
            self.entry.delete(0, 'end')
            self.entry.insert('end', 'Error: Empty input')
        elif self.validate_expression(expression):
            try:
                result = str(self.calculator.eval_expr(expression))
                self.entry.delete(0, 'end')
                self.entry.insert('end', result)
            except ZeroDivisionError:
                self.entry.delete(0, 'end')
                self.entry.insert('end', 'Error: Division by zero')
            except Exception as e:
                self.entry.delete(0, 'end')
                self.entry.insert('end', 'Error: ' + str(e))
        else:
            self.entry.delete(0, 'end')
            self.entry.insert('end', 'Invalid input')

    def clear(self):
        self.entry.delete(0, 'end')

    def validate_expression(self, expression):
        return all(char.isnumeric() or char.isspace() or char in '().+-*/^' for char in expression)

    def run(self):
        self.window.mainloop()

def main():
    calc = Calculator()
    gui = CalculatorGUI(calc)
    gui.run()

if __name__ == "__main__":
    main()
