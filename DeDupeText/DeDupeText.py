import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import logging
import os
import shutil

def calculate_checksum(filename):
    """Calculate the SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def read_file(filename):
    """Read the contents of a file."""
    try:
        with open(filename, 'r') as f:
            return f.readlines()
    except IOError as e:
        logging.error(f"Error reading file: {e}")
        messagebox.showerror("File Read Error", f"Error occurred while reading the file: {e}")
        return None

def write_file(filename, lines):
    """Write lines to a file."""
    try:
        with open(filename, 'w') as f:
            f.writelines(lines)
    except IOError as e:
        logging.error(f"Error writing file: {e}")
        messagebox.showerror("File Write Error", f"Error occurred while writing to the file: {e}")
        return False
    return True

def backup_file(original_file):
    """Create a backup of the file."""
    backup_file = f"{original_file}.bak"
    try:
        shutil.copy(original_file, backup_file)
        logging.info(f"Backup created: {backup_file}")
    except IOError as e:
        logging.error(f"Failed to create backup: {e}")
        messagebox.showerror("Backup Error", f"Failed to create a backup of the file: {e}")
        return False
    return True

def remove_duplicates_from_file(filename):
    """Remove duplicate lines from a file."""
    logging.info(f"Processing the file: {filename} to identify duplicate lines.")
    messagebox.showinfo("Processing", f"Processing the file: {filename} to identify duplicate lines.")
    
    if not backup_file(filename):
        return

    initial_checksum = calculate_checksum(filename)

    lines = read_file(filename)
    if lines is None:
        return

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

    if write_file(filename, unique_lines):
        messagebox.showinfo("Success", "Duplicates have been successfully removed from the file!")

    final_checksum = calculate_checksum(filename)
    if initial_checksum == final_checksum:
        messagebox.showinfo("Info", "No duplicates were found or removed.")

def verify_program():
    """Verify the functionality of the program."""
    temp_filename = "temp_readme.txt"
    with open(temp_filename, 'w') as f:
        f.writelines(["This is a test line.\n",
                      "This is a duplicate test line.\n",
                      "This is a test line.\n",  # Duplicate line
                      "This is another test line.\n"])

    remove_duplicates_from_file(temp_filename)

    lines = read_file(temp_filename)
    if lines is None:
        return

    os.remove(temp_filename)

    if len(lines) == 3 and lines.count("This is a test line.\n") == 1:
        messagebox.showinfo("Verification", "Verification Complete: The program is functioning correctly!")
    else:
        messagebox.showerror("Verification", "Verification Failed: There seems to be an issue with the program's functionality.")

def main():
    """Main function to run the program."""
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    root.withdraw()

    verify_program()

    while True:
        filename = filedialog.askopenfilename(title="Select a text file to remove duplicates", filetypes=[("Text files", "*.txt")])
        if not filename:
            messagebox.showinfo("Exit", "Thank you for using the Duplicate Remover tool. Goodbye!")
            break

        remove_duplicates_from_file(filename)

if __name__ == "__main__":
    main()