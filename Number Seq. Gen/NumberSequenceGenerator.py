from time import sleep
from typing import Generator
import random

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
    print("Welcome to the Magic Number Game!")
    print("I'll generate a sequence of numbers and then you think of any number in that range.")
    print("Then, I'll try to magically guess the number you're thinking of!\n")

    start = get_integer_input("Enter the start of the sequence: ")
    end = get_integer_input("Enter the end of the sequence: ")
    step = get_integer_input("Enter the step size: ")

    print("Now, think of a number within the generated sequence but don't tell me!")
    sleep(2)

    display_all = input("Do you want to display the numbers all at once (y/n)? ").lower()

    if display_all == "y":
        print("Here's the sequence of numbers:", list(generate_sequence(start, end, step)))
    else:
        print("Displaying the numbers one by one:")
        for number in generate_sequence(start, end, step):
            print(number, end=" ", flush=True)
            sleep(1)
        print()

    input("\nHave your number in mind? Press Enter when ready...")

    # Pretend to think hard
    print("I'm thinking...")
    sleep(2)

    # Randomly guess a number from the sequence (for fun!)
    guess = random.choice(list(generate_sequence(start, end, step)))

    print(f"Is your magic number {guess}?")
    response = input("Am I right (y/n)? ").lower()

    if response == "y":
        print("Hooray! I'm truly magical! 🌟")
    else:
        print("Aww, better luck next time. Keep the magic alive! ✨")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()