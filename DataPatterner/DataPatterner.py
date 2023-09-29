import re
import os

def prompt_file_path(message: str) -> str:
    """Prompt user for a file path and validate its existence."""
    while True:
        file_path = input(message)
        if os.path.isfile(file_path):
            return file_path
        print(f"File '{file_path}' not found. Please enter a valid path.")

def prompt_for_regex() -> str:
    """Prompt user for a regex pattern and validate it."""
    while True:
        regex = input("Enter the regex pattern: ")
        try:
            re.compile(regex)
            return regex
        except re.error:
            print("Invalid regex pattern. Please try again.")

def read_input_file(file_path: str) -> list[str]:
    """Read and return the content of the input file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except IOError as e:
        print(f"Error reading file: {e}")
        return []

def write_to_output_file(file_path: str, data: list[str]):
    """Write parsed data to the output file with overwrite confirmation."""
    while True:
        if os.path.exists(file_path) and input(f"'{file_path}' already exists. Overwrite? (y/n): ").lower() != 'y':
            print("Operation aborted.")
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(f"{line}\n" for line in data)
            print(f"Data written to '{file_path}'")
            break
        except IOError as e:
            print(f"Error writing to file: {e}. Please try again or provide a different output file path.")
            file_path = input("Enter a different output file path or the same to retry: ")

def parse_data(content: list[str], regex_pattern: str) -> list[str]:
    """Parse and return data lines based on the provided regex pattern."""
    return [match.group(0) for line in content if (match := re.search(regex_pattern, line))]

def test_pattern_on_sample(content: list[str], regex_pattern: str):
    """Test regex pattern on sample lines and display results."""
    for sample in content[:5]:
        match = re.search(regex_pattern, sample)
        print(f"Original Line: {sample.strip()}")
        print(f"Matched: {match.group(0)}\n" if match else "No Match\n")

def process_parsing():
    """Parse data based on the user's regex pattern."""
    input_file = prompt_file_path("Enter the input data file path: ")
    output_file = input("Enter the output file path: ")
    regex_pattern = prompt_for_regex()

    content = read_input_file(input_file)
    parsed_data = parse_data(content, regex_pattern)

    if not parsed_data:
        print("No matches found using the provided regex pattern.")
        return

    write_to_output_file(output_file, parsed_data)

def test_pattern():
    """Test regex pattern on sample data."""
    input_file = prompt_file_path("Enter the sample data file path: ")
    regex_pattern = prompt_for_regex()

    content = read_input_file(input_file)
    test_pattern_on_sample(content, regex_pattern)

def main():
    """Main function for user interactions."""
    print("Welcome to the Data Parser!")

    menu = {
        '1': ("Parse Data", process_parsing),
        '2': ("Test Pattern on Sample Data", test_pattern),
        '3': ("Exit", None)
    }

    while True:
        print("\nMenu:")
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")

        choice = input("\nEnter your choice (1-3): ")

        if choice in menu:
            _, action = menu[choice]
            if action:
                action()
            else:
                break
        else:
            print("Invalid choice. Please select from the given options.")

if __name__ == "__main__":
    main()