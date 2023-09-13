import re
import os

def prompt_file_path(message):
    """Prompts the user for a file path and checks if it exists."""
    while True:
        file_path = input(message)
        if os.path.exists(file_path):
            return file_path
        print(f"File '{file_path}' not found. Please enter a valid path.")

def prompt_for_regex():
    """Prompts the user for a regex pattern."""
    while True:
        try:
            regex = input("Enter the regex pattern: ")
            re.compile(regex)
            return regex
        except re.error:
            print("Invalid regex pattern. Please try again.")

def read_input_file(file_path):
    """Reads the content of the input file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def write_to_output_file(file_path, data):
    """Writes parsed data to the output file, with overwrite confirmation."""
    if os.path.exists(file_path) and input(f"'{file_path}' already exists. Do you want to overwrite? (y/n): ").lower() != 'y':
        print("Operation aborted.")
        return

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(f"{line}\n" for line in data)
        print(f"Data written to '{file_path}'")
    except Exception as e:
        print(f"Error writing to file: {e}")

def parse_data(content, regex_pattern):
    """Parses data lines based on the provided regex pattern."""
    return [match.group(0) for line in content if (match := re.search(regex_pattern, line))]

def test_pattern_on_sample(content, regex_pattern):
    """Tests regex pattern on sample lines for user verification."""
    for sample in content[:5]:
        match = re.search(regex_pattern, sample)
        print(f"Original Line: {sample.strip()}")
        print(f"Matched: {match.group(0)}\n" if match else "No Match\n")

def process_parsing():
    input_file = prompt_file_path("Enter the path to the input data file: ")
    output_file = input("Enter the path to the output file: ")
    regex_pattern = prompt_for_regex()

    content = read_input_file(input_file)
    parsed_data = parse_data(content, regex_pattern)

    if not parsed_data:
        print("No matches found using the provided regex pattern.")
        return

    write_to_output_file(output_file, parsed_data)

def test_pattern():
    input_file = prompt_file_path("Enter the path to the sample data file: ")
    regex_pattern = prompt_for_regex()

    content = read_input_file(input_file)
    test_pattern_on_sample(content, regex_pattern)

def main():
    print("Welcome to the Data Parser!")

    while True:
        print("\nMenu:")
        print("1. Parse Data")
        print("2. Test Pattern on Sample Data")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == '1':
            process_parsing()
        elif choice == '2':
            test_pattern()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select from the given options.")

if __name__ == "__main__":
    main()
