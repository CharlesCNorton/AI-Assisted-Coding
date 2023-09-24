import tkinter as tk
from tkinter import filedialog
import hashlib
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)

def calculate_checksum(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def read_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()

def write_file(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line)

def remove_duplicates_from_file(filename):
    logging.info(f"Processing {filename} to remove duplicates.")

    # Initial checksum
    initial_checksum = calculate_checksum(filename)

    # Read and detect duplicates
    try:
        lines = read_file(filename)
        total_lines = len(lines)
        unique_lines = list(set(lines))
        duplicates = total_lines - len(unique_lines)
        
        print(f"Total lines: {total_lines}")
        print(f"Duplicate lines: {duplicates}")
        proceed = input("Do you want to remove duplicates? (y/n): ")
        if proceed.lower() != 'y':
            print("Operation canceled.")
            return
        write_file(filename, unique_lines)
    except FileNotFoundError:
        logging.error(f"The file {filename} was not found.")
        print(f"The file {filename} was not found.")
        return
    except PermissionError:
        logging.error(f"Permission denied while trying to access {filename}.")
        print(f"Permission denied while trying to access {filename}.")
        return
    except Exception as e:
        logging.error(f"An unknown error occurred: {e}")
        print(f"An unknown error occurred: {e}")
        return
    else:
        # Final checksum
        final_checksum = calculate_checksum(filename)

        # Report
        if initial_checksum != final_checksum:
            logging.info(f"Successfully removed duplicates from {filename}.")
            print(f"Successfully removed duplicates from {filename}.")
        else:
            logging.info(f"No duplicates found in {filename}.")
            print(f"No duplicates found in {filename}.")

def main():
    root = tk.Tk()
    root.withdraw()

    while True:
        print("1. Remove duplicates from a file")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            filename = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text files", "*.txt")])
            if filename and os.path.exists(filename):
                remove_duplicates_from_file(filename)
            else:
                logging.warning("No valid file selected. Please try again.")
                print("No valid file selected. Please try again.")
        elif choice == '2':
            logging.info("Exiting the program. Goodbye!")
            print("Exiting the program. Goodbye!")
            break
        else:
            logging.warning("Invalid choice entered.")
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()