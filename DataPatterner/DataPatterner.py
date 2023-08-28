import re
import os

def read_input_file(file_path):
    """Reads the content of the input file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def write_to_output_file(file_path, data):
    """Writes parsed data to the output file, with overwrite confirmation."""
    if os.path.exists(file_path):
        overwrite = input(f"{file_path} already exists. Do you want to overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation aborted.")
            return

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in data:
                file.write(line + '\n')
        print(f"Data written to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def parse_data(content, regex_pattern):
    """Parses data lines based on the provided regex pattern."""
    parsed_data = []
    for line in content:
        try:
            match = re.search(regex_pattern, line)
            if match:
                parsed_data.append(match.group(0))
        except re.error:
            print("Invalid regex pattern.")
            return []
    return parsed_data

def test_pattern_on_sample(content, regex_pattern):
    """Tests regex pattern on sample lines for user verification."""
    test_samples = content[:5]  # Taking the first 5 lines as samples
    for sample in test_samples:
        try:
            match = re.search(regex_pattern, sample)
            if match:
                print(f"Original Line: {sample.strip()}")
                print(f"Matched: {match.group(0)}\n")
            else:
                print(f"Original Line: {sample.strip()}")
                print("No Match\n")
        except re.error:
            print("Invalid regex pattern.")
            return

def main():
    print("Welcome to the Data Parser!")

    while True:
        print("\nMenu:")
        print("1. Parse Data")
        print("2. Test Pattern on Sample Data")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            input_file = input("Enter the path to the input data file: ")
            if not os.path.exists(input_file):
                print(f"File {input_file} not found.")
                continue

            output_file = input("Enter the path to the output file: ")

            regex_pattern = input("Enter the regex pattern: ")

            content = read_input_file(input_file)
            parsed_data = parse_data(content, regex_pattern)

            if not parsed_data:
                print("No matches found using the provided regex pattern.")
                continue

            write_to_output_file(output_file, parsed_data)

        elif choice == '2':
            input_file = input("Enter the path to the sample data file: ")
            if not os.path.exists(input_file):
                print(f"File {input_file} not found.")
                continue

            regex_pattern = input("Enter the regex pattern to test: ")

            content = read_input_file(input_file)
            test_pattern_on_sample(content, regex_pattern)

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please select from the given options.")

if __name__ == "__main__":
    main()
