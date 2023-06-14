"""
This program is a highly-enhanced, object-oriented calculator that can perform a range of arithmetic operations.
The calculator was improved with the assistance of GPT-4 and Bard on 2023-06-08.
"""
import tkinter as tk
import math
import re
import keyword
class Calculator:
    """A calculator class that can perform a range of arithmetic operations."""
    def __init__(self):
        self.history = []
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'g': 9.81,  # acceleration due to gravity
            'c': 299792458,  # speed of light in m/s
            'h': 6.62607015e-34  # Planck's constant in m^2 kg / s
        }
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
                    if button in self.calculator.constants:
                        btn = tk.Button(self.window, text=button, width=5, height=2, font=('Arial', 12), command=lambda x=button: self.handle_button_click(str(self.calculator.constants[x])))
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
        expression = self.entry.get()
        if self.validate_expression(expression):
            try:
                result = str(eval(expression))
                self.entry.delete(0, 'end')
                self.entry.insert('end', result)
            except ZeroDivisionError:
                self.entry.delete(0, 'end')
                self.entry.insert('end', 'Error: Division by zero')
            except SyntaxError:
                self.entry.delete(0, 'end')
                self.entry.insert('end', 'Error: Syntax error')
            except ValueError:
                self.entry.delete(0, 'end')
                self.entry.insert('end', 'Error: Invalid value')
            except TypeError:
                self.entry.delete(0, 'end')
                self.entry.insert('end', 'Error: Invalid operation')
            except Exception as e:
                self.entry.delete(0, 'end')
                self.entry.insert('end', 'Error: ' + str(e))
        else:
            self.entry.delete(0, 'end')
            self.entry.insert('end', 'Invalid input')
    def clear(self):
        self.entry.delete(0, 'end')
    def validate_expression(self, expression):
        if any(kw in expression for kw in keyword.kwlist):
            return False
        if expression.count('(') != expression.count(')'):
            return False
        if not re.match("^[-+*/.\d\s()^sqrtlogsinetcospie]+$", expression):
            return False
        return True
    def run(self):
        self.window.mainloop()
def main():
    calc = Calculator()
    gui = CalculatorGUI(calc)
    gui.run()
if __name__ == "__main__":
    main()
