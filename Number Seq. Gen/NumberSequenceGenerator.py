from typing import Generator
from time import sleep
import random
from colorama import Fore, Style, init

init(autoreset=True)

def generate_sequence(start: int, end: int, step: int = 1) -> Generator[int, None, None]:
    while start <= end:
        yield start
        start += step

def get_integer_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter an integer.")

def main() -> None:
    print(Fore.CYAN + "\nWelcome to the Magic Number Game!")
    print("I'll generate a sequence of numbers and then you think of any number in that range.")
    print("Then, I'll try to magically guess the number you're thinking of!\n")

    start = get_integer_input(Fore.MAGENTA + "Enter the start of the sequence: ")
    end = get_integer_input(Fore.MAGENTA + "Enter the end of the sequence: ")
    step = get_integer_input(Fore.MAGENTA + "Enter the step size: ")

    print(Fore.YELLOW + "\nNow, think of a number within the generated sequence but don't tell me!")
    sleep(2)

    display_all = input(Fore.GREEN + "Do you want to display the numbers all at once (y/n)? ").lower()

    if display_all == "y":
        print(Fore.YELLOW + "Here's the sequence of numbers:", list(generate_sequence(start, end, step)))
    else:
        print(Fore.YELLOW + "Displaying the numbers one by one:")
        for number in generate_sequence(start, end, step):
            print(number, end=" ", flush=True)
            sleep(1)
        print()

    input(Fore.YELLOW + "\nHave your number in mind? Press Enter when ready...")

    print(Fore.BLUE + "I'm thinking...")
    sleep(2)

    guess = random.choice(list(generate_sequence(start, end, step)))

    print(Fore.CYAN + f"Is your magic number {guess}?")
    response = input(Fore.GREEN + "Am I right (y/n)? ").lower()

    if response == "y":
        print(Fore.GREEN + "Hooray! I'm truly magical! 🌟")
    else:
        print(Fore.RED + "Aww, better luck next time. Keep the magic alive! ✨")

    input(Fore.CYAN + "Press Enter to exit...")

if __name__ == "__main__":
    main()