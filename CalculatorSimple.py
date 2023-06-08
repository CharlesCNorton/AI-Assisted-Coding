{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPdH04YQu66DDzVZF35bbnD"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "zrr0LHL6h-g9",
        "outputId": "e45b86ec-119f-43a2-dab1-a06940b5cbe1"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Welcome to the enhanced calculator!\n",
            "You can perform basic operations: +, -, *, /\n",
            "And scientific operations: ^ (power), sqrt (square root), log (natural logarithm), sin, cos, tan\n",
            "For scientific operations, only the first number will be considered\n",
            "Enter the first number: 1\n",
            "Enter the second number: 1\n",
            "Enter the operation (+, -, *, /, ^, sqrt, log, sin, cos, tan): sin\n",
            "The result is: 0.8414709848078965\n",
            "Continue calculating (y/n)? y\n",
            "Enter the first number: 4\n",
            "Enter the second number: 7\n",
            "Enter the operation (+, -, *, /, ^, sqrt, log, sin, cos, tan): +\n",
            "The result is: 11.0\n"
          ]
        }
      ],
      "source": [
        "\"\"\"\n",
        "This program is a highly-enhanced, object-oriented calculator that can perform a range of arithmetic operations.\n",
        "The calculator was improved with the assistance of GPT-4 and Bard on 2023-06-08.\n",
        "\"\"\"\n",
        "\n",
        "# Import the necessary modules\n",
        "import math\n",
        "\n",
        "class Calculator:\n",
        "    \"\"\"A calculator class that can perform a range of arithmetic operations.\"\"\"\n",
        "    \n",
        "    def __init__(self):\n",
        "        self.history = []\n",
        "\n",
        "    def calculate(self, operation, operand1, operand2=0):\n",
        "        # Perform the appropriate calculation based on operation\n",
        "        operations = {\n",
        "            \"+\": operand1 + operand2,\n",
        "            \"-\": operand1 - operand2,\n",
        "            \"*\": operand1 * operand2,\n",
        "            \"/\": operand1 / operand2 if operand2 != 0 else 'Error: Division by zero',\n",
        "            \"^\": operand1 ** operand2,\n",
        "            \"sqrt\": math.sqrt(operand1) if operand1 >= 0 else 'Error: Square root of negative number',\n",
        "            \"log\": math.log(operand1) if operand1 > 0 else 'Error: Logarithm of non-positive number',\n",
        "            \"sin\": math.sin(operand1),\n",
        "            \"cos\": math.cos(operand1),\n",
        "            \"tan\": math.tan(operand1)\n",
        "        }\n",
        "        result = operations.get(operation, \"Invalid operation. Please enter a valid operation.\")\n",
        "        if isinstance(result, float):\n",
        "            # Add calculation to history\n",
        "            self.history.append((operation, operand1, operand2, result))\n",
        "        return result\n",
        "\n",
        "    def show_history(self):\n",
        "        # Show the history of all calculations\n",
        "        for i, item in enumerate(self.history):\n",
        "            operation, operand1, operand2, result = item\n",
        "            print(f\"{i+1}: {operand1} {operation} {operand2} = {result}\")\n",
        "\n",
        "def main():\n",
        "    \"\"\"Main function to run the calculator in a loop.\"\"\"\n",
        "    print(\"Welcome to the enhanced calculator!\")\n",
        "    print(\"Type 'help' for a list of available operations, 'history' to see all past calculations, or 'exit' to quit.\")\n",
        "\n",
        "    calc = Calculator()\n",
        "\n",
        "    while True:\n",
        "        user_input = input(\"\\nEnter your operation: \")\n",
        "\n",
        "        if user_input.lower() == 'exit':\n",
        "            break\n",
        "        elif user_input.lower() == 'history':\n",
        "            calc.show_history()\n",
        "            continue\n",
        "        elif user_input.lower() == 'help':\n",
        "            print(\"Available operations: +, -, *, /, ^ (power), sqrt (square root), log (natural logarithm), sin, cos, tan\")\n",
        "            continue\n",
        "\n",
        "        try:\n",
        "            operation, operand1, operand2 = user_input.split()\n",
        "            operand1 = float(operand1)\n",
        "            operand2 = float(operand2)\n",
        "        except ValueError:\n",
        "            print(\"Invalid input. Please enter operation and two numbers separated by spaces (for example, '+ 1 2'). For single operand operations like sqrt, log, sin, cos, tan, the second number can be 0.\")\n",
        "            continue\n",
        "\n",
        "        result = calc.calculate(operation, operand1, operand2)\n",
        "\n",
        "        if \"Error\" not in str(result) and \"Invalid\" not in str(result):\n",
        "            print(\"The result is:\", result)\n",
        "        else:\n",
        "            print(result)\n",
        "\n",
        "# Run the main function\n",
        "if __name__ == \"__main__\":\n",
        "    main()\n"
      ]
    }
  ]
}