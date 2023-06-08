"""
This program is a highly-enhanced, object-oriented calculator that can perform a range of arithmetic operations.
The calculator was improved with the assistance of GPT-4 and Bard on 2023-06-08.
"""

# Import the necessary modules
import math

class Calculator:
    """A calculator class that can perform a range of arithmetic operations."""
    
    def __init__(self):
        self.history = []

    def calculate(self, operation, operand1, operand2=0):
        # Perform the appropriate calculation based on operation
        operations = {
            "+": operand1 + operand2,
            "-": operand1 - operand2,
            "*": operand1 * operand2,
            "/": operand1 / operand2 if operand2 != 0 else 'Error: Division by zero',
            "^": operand1 ** operand2,
            "sqrt": math.sqrt(operand1) if operand1 >= 0 else 'Error: Square root of negative number',
            "log": math.log(operand1) if operand1 > 0 else 'Error: Logarithm of non-positive number',
            "sin": math.sin(operand1),
            "cos": math.cos(operand1),
            "tan": math.tan(operand1)
        }
        result = operations.get(operation, "Invalid operation. Please enter a valid operation.")
        if isinstance(result, float):
            # Add calculation to history
            self.history.append((operation, operand1, operand2, result))
        return result

    def show_history(self):
        # Show the history of all calculations
        for i, item in enumerate(self.history):
            operation, operand1, operand2, result = item
            print(f"{i+1}: {operand1} {operation} {operand2} = {result}")

def main():
    """Main function to run the calculator in a loop."""
    print("Welcome to the enhanced calculator!")
    print("Type 'help' for a list of available operations, 'history' to see all past calculations, or 'exit' to quit.")

    calc = Calculator()

    while True:
        user_input = input("\nEnter your operation: ")

        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'history':
            calc.show_history()
            continue
        elif user_input.lower() == 'help':
            print("Available operations: +, -, *, /, ^ (power), sqrt (square root), log (natural logarithm), sin, cos, tan")
            continue

        try:
            operation, operand1, operand2 = user_input.split()
            operand1 = float(operand1)
            operand2 = float(operand2)
        except ValueError:
            print("Invalid input. Please enter operation and two numbers separated by spaces (for example, '+ 1 2'). For single operand operations like sqrt, log, sin, cos, tan, the second number can be 0.")
            continue

        result = calc.calculate(operation, operand1, operand2)

        if "Error" not in str(result) and "Invalid" not in str(result):
            print("The result is:", result)
        else:
            print(result)

# Run the main function
if __name__ == "__main__":
    main()
