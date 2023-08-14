
"""
This program generates a continuous sequence of numbers from start to end, with an optional step size.

The user can choose to display the numbers all at once or one by one.
"""

from time import sleep
from typing import Generator

def generate_sequence(start: int, end: int, step: int = 1) -> Generator[int, None, None]:
    """Generates a continuous sequence of numbers from start to end, with an optional step size."""
    while start <= end:
        yield start
        start += step

def get_integer_input(prompt: str) -> int:
    """Prompts the user for integer input and handles invalid responses."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main() -> None:
    """Main function to execute the program."""
    start = get_integer_input("Enter the start of the sequence: ")
    end = get_integer_input("Enter the end of the sequence: ")
    step = get_integer_input("Enter the step size: ")

    display_all = input("Do you want to display the numbers all at once (y/n)? ").lower()

    if display_all == "y":
        print("The sequence of numbers is:", list(generate_sequence(start, end, step)))
    else:
        for number in generate_sequence(start, end, step):
            print(number, end=" ", flush=True)
            sleep(1)
        print()

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
