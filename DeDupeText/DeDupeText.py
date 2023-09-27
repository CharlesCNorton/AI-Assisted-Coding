import tkinter as tk
from tkinter import filedialog
import hashlib
import logging
import os

def calculate_checksum(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def read_write_file(filename, mode, lines=None):
    with open(filename, mode) as f:
        if mode == 'r':
            return f.readlines()
        elif mode == 'w':
            for line in lines:
                f.write(line)

def remove_duplicates_from_file(filename):
    logging.info(f"Processing {filename} to remove duplicates.")
    initial_checksum = calculate_checksum(filename)
    try:
        lines = read_write_file(filename, 'r')
        total_lines = len(lines)
        unique_lines = list(set(lines))
        duplicates = total_lines - len(unique_lines)

        print(f"Total lines: {total_lines}")
        print(f"Duplicate lines: {duplicates}")
        proceed = input("Do you want to remove duplicates? (y/n): ")
        if proceed.lower() != 'y':
            print("Operation canceled.")
            return

        read_write_file(filename, 'w', unique_lines)

    except (FileNotFoundError, PermissionError, Exception) as e:
        logging.error(f"{type(e).__name__} occurred: {e}")
        print(f"{type(e).__name__} occurred: {e}")
        return

    final_checksum = calculate_checksum(filename)
    if initial_checksum != final_checksum:
        logging.info(f"Successfully removed duplicates from {filename}.")
        print(f"Successfully removed duplicates from {filename}.")
    else:
        logging.info(f"No duplicates found in {filename}.")
        print(f"No duplicates found in {filename}.")

def main():
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    root.withdraw()

    menu_actions = {'1': lambda: remove_duplicates_from_file(
                                filedialog.askopenfilename(title="Select a text file",
                                                           filetypes=[("Text files", "*.txt")])
                               ),
                    '2': lambda: print("Exiting the program. Goodbye!")}

    while True:
        print("1. Remove duplicates from a file")
        print("2. Exit")
        choice = input("Enter your choice: ")

        action = menu_actions.get(choice)
        if action:
            action()
            if choice == '2':
                break
        else:
            logging.warning("Invalid choice entered.")
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
