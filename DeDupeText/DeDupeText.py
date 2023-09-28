import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import logging
import os

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
    logging.info(f"Processing the file: {filename} to identify duplicate lines.")
    messagebox.showinfo("Processing", f"Processing the file: {filename} to identify duplicate lines.")

    initial_checksum = calculate_checksum(filename)

    try:
        lines = read_file(filename)
        unique_lines = sorted(set(lines), key=lines.index)

        total_lines = len(lines)
        duplicates = total_lines - len(unique_lines)

        msg = (f"File Analysis Complete!\n\n"
               f"Total lines: {total_lines}\n"
               f"Duplicate lines found: {duplicates}\n\n"
               f"Do you want to remove the duplicate lines?")
        proceed = messagebox.askyesno("Duplicate Analysis", msg)

        if not proceed:
            logging.info("User opted to cancel the operation.")
            messagebox.showinfo("Cancelled", "You chose not to remove duplicates. No changes made to the file.")
            return

        write_file(filename, unique_lines)
        messagebox.showinfo("Success", "Duplicates have been successfully removed from the file!")

    except (FileNotFoundError, PermissionError) as e:
        logging.error(f"{type(e).__name__} occurred: {e}")
        messagebox.showerror("Error", f"{type(e).__name__} occurred: {e}")
        return
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}")
        return

    final_checksum = calculate_checksum(filename)
    if initial_checksum == final_checksum:
        messagebox.showinfo("Info", "After analysis, no duplicates were found in the selected file.")

def verify_program():
    # Create a temporary test file with duplicate lines
    temp_filename = "temp_readme.txt"
    with open(temp_filename, 'w') as f:
        f.write("This is a test line.\n")
        f.write("This is a duplicate test line.\n")
        f.write("This is a test line.\n")  # This is a duplicate line
        f.write("This is another test line.\n")

    remove_duplicates_from_file(temp_filename)

    # Check if the duplicate line has been removed
    with open(temp_filename, 'r') as f:
        lines = f.readlines()

    os.remove(temp_filename)  # Clean up the temporary file

    if len(lines) == 3 and lines.count("This is a test line.\n") == 1:
        messagebox.showinfo("Verification", "Verification Complete: The program is functioning correctly!")
    else:
        messagebox.showerror("Verification", "Verification Failed: There seems to be an issue with the program's functionality.")

def main():
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    root.withdraw()

    verify_program()  # Verify that the program works correctly

    while True:
        filename = filedialog.askopenfilename(title="Select a text file to remove duplicates", filetypes=[("Text files", "*.txt")])
        if not filename:
            messagebox.showinfo("Exit", "Thank you for using the Duplicate Remover tool. Goodbye!")
            break

        remove_duplicates_from_file(filename)

if __name__ == "__main__":
    main()
