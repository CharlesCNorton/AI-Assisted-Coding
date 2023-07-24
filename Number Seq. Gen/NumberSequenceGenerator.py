"""
This program generates a continuous sequence of numbers from start to end, with an optional step size.

The user can choose to display the numbers all at once or one by one.

It was created with Google Bard on 2023-06-08 at 10:30 AM PST and modified by OpenAI Assistant on 2023-07-23.

Improvements:

Added error handling for invalid input
Modified the printout for "display all at once" to show the entire sequence instead of the generator object.
Attributions:

The sleep function was imported from the time module.
The typing module was used to add type annotations to the code.
"""

from time import sleep
from typing import Iterable

def generate_sequence(start: int, end: int, step: int = 1) -> Iterable[int]:
"""Generates a continuous sequence of numbers from start to end, with an optional step size.

Args:
start: The start of the sequence.
end: The end of the sequence.
step: The step size.

Returns:
A generator that yields the numbers in the sequence.
"""

while start <= end:
yield start
start += step

def get_input(prompt: str) -> int:
"""Prompts the user for integer input and handles invalid responses.

Args:
prompt: The input prompt to display to the user.

Returns:
The user's input as an integer.
"""
while True:
try:
return int(input(prompt))
except ValueError:
print("Invalid input. Please enter an integer.")

def main() -> None:
"""The main function."""

start = get_input("Enter the start of the sequence: ")
end = get_input("Enter the end of the sequence: ")
step = get_input("Enter the step size: ")

sequence = generate_sequence(start, end, step)

display_all = input("Do you want to display the numbers all at once (y/n)? ")

if display_all == "y":
print("The sequence of numbers is:", list(sequence))
else:
for number in sequence:
print(number, end=" ")
sleep(1)
print()

if name == "main":
main()
