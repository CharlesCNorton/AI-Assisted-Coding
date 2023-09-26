# Import the required libraries
import tkinter as tk  # For GUI interactions
from tkinter import filedialog  # File dialog for file selection
import hashlib  # For generating hash/checksum
import logging  # For logging
import os  # For file operations

# Initialize the logging framework with an INFO level
logging.basicConfig(level=logging.INFO)

# Function to calculate the SHA-256 checksum of a file
def calculate_checksum(filename):
    sha256_hash = hashlib.sha256()  # Initialize SHA-256 hash object
    with open(filename, "rb") as f:  # Open file in read-binary mode
        for byte_block in iter(lambda: f.read(4096), b""):  # Read 4096 bytes at a time
            sha256_hash.update(byte_block)  # Update the hash object
    return sha256_hash.hexdigest()  # Return the hexadecimal digest

# Function to read all lines from a text file
def read_file(filename):
    with open(filename, 'r') as f:  # Open file in read mode
        return f.readlines()  # Read and return all lines

# Function to write lines to a text file
def write_file(filename, lines):
    with open(filename, 'w') as f:  # Open file in write mode
        for line in lines:  # Loop through each line
            f.write(line)  # Write the line to the file

# Function to remove duplicate lines from a text file
def remove_duplicates_from_file(filename):
    logging.info(f"Processing {filename} to remove duplicates.")  # Log the operation

    # Calculate initial checksum of the file for comparison later
    initial_checksum = calculate_checksum(filename)

    try:
        # Read lines from the file
        lines = read_file(filename)
        total_lines = len(lines)  # Count total lines

        # Remove duplicate lines
        unique_lines = list(set(lines))
        duplicates = total_lines - len(unique_lines)  # Count duplicate lines

        # Display statistics
        print(f"Total lines: {total_lines}")
        print(f"Duplicate lines: {duplicates}")

        # Confirm action from the user
        proceed = input("Do you want to remove duplicates? (y/n): ")
        if proceed.lower() != 'y':
            print("Operation canceled.")
            return  # Exit the function if user denies

        # Write back the unique lines to the file
        write_file(filename, unique_lines)

    # Handle specific exceptions
    except FileNotFoundError:
        logging.error(f"The file {filename} was not found.")
        print(f"The file {filename} was not found.")
        return
    except PermissionError:
        logging.error(f"Permission denied while trying to access {filename}.")
        print(f"Permission denied while trying to access {filename}.")
        return
    except Exception as e:  # Catch-all for other exceptions
        logging.error(f"An unknown error occurred: {e}")
        print(f"An unknown error occurred: {e}")
        return
    else:
        # Calculate the final checksum
        final_checksum = calculate_checksum(filename)

        # Log and display the operation's result
        if initial_checksum != final_checksum:
            logging.info(f"Successfully removed duplicates from {filename}.")
            print(f"Successfully removed duplicates from {filename}.")
        else:
            logging.info(f"No duplicates found in {filename}.")
            print(f"No duplicates found in {filename}.")

# Main function to run the program
def main():
    root = tk.Tk()  # Initialize Tkinter root window
    root.withdraw()  # Hide the Tkinter root window

    # Loop for the menu
    while True:
        # Display options
        print("1. Remove duplicates from a file")
        print("2. Exit")
        choice = input("Enter your choice: ")

        # Perform actions based on user's choice
        if choice == '1':
            filename = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text files", "*.txt")])
            if filename and os.path.exists(filename):  # Check if a valid file is selected
                remove_duplicates_from_file(filename)
            else:
                logging.warning("No valid file selected. Please try again.")
                print("No valid file selected. Please try again.")
        elif choice == '2':
            logging.info("Exiting the program. Goodbye!")
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and end the program
        else:
            logging.warning("Invalid choice entered.")
            print("Invalid choice. Please try again.")

# Entry point of the script
if __name__ == "__main__":
    main()  # Call the main function
