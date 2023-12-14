import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import logging
import os
import shutil

def file_exists(filename):
    return os.path.exists(filename)

def calculate_checksum(filename):
    if not file_exists(filename):
        logging.error(f"File not found: {filename}")
        return None
    sha256_hash = hashlib.sha256()
    try:
        with open(filename, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                sha256_hash.update(byte_block)
    except IOError as e:
        logging.error(f"Error reading file for checksum: {e}")
        return None
    return sha256_hash.hexdigest()

def file_operation(operation, filename, mode='r', data=None):
    if not file_exists(filename) and mode == 'r':
        logging.error(f"File not found: {filename}")
        messagebox.showerror("File Error", f"File not found: {filename}")
        return None if mode == 'r' else False

    try:
        with open(filename, mode) as file:
            return operation(file, data)
    except IOError as e:
        action = 'reading' if mode == 'r' else 'writing'
        logging.error(f"Error {action} file: {e}")
        messagebox.showerror(f"File {action.capitalize()} Error", f"Error occurred while {action} the file: {e}")
        return None if mode == 'r' else False

def read_file(file, _):
    return file.readlines()

def write_file(file, lines):
    file.writelines(lines)
    return True

def backup_file(original_file):
    backup_file = f"{original_file}.bak"
    if file_exists(backup_file):
        logging.warning(f"Backup file already exists: {backup_file}")
        messagebox.showwarning("Backup Warning", f"Backup file already exists and will be overwritten: {backup_file}")
    try:
        shutil.copy(original_file, backup_file)
        logging.info(f"Backup created: {backup_file}")
    except IOError as e:
        logging.error(f"Failed to create backup: {e}")
        messagebox.showerror("Backup Error", f"Failed to create a backup of the file: {e}")
        return False
    return True

def remove_duplicates_from_file(filename):
    logging.info(f"Processing the file: {filename} to identify duplicate lines.")
    messagebox.showinfo("Processing", f"Processing the file: {filename} to identify duplicate lines.")

    if not backup_file(filename):
        return

    initial_checksum = calculate_checksum(filename)
    if initial_checksum is None:
        return

    # Efficient handling of large files using a set
    unique_lines = set()
    try:
        with open(filename, 'r') as file:
            for line in file:
                unique_lines.add(line)
    except IOError as e:
        logging.error(f"Error reading file for duplicate removal: {e}")
        messagebox.showerror("Read Error", f"Error occurred while reading the file: {e}")
        return

    total_lines = len(unique_lines)
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

    if file_operation(write_file, filename, 'w', list(unique_lines)):
        messagebox.showinfo("Success", "Duplicates have been successfully removed from the file!")

    final_checksum = calculate_checksum(filename)
    if final_checksum is None or initial_checksum == final_checksum:
        messagebox.showinfo("Info", "No duplicates were found or removed.")

def verify_program():
    temp_filename = "temp_readme.txt"
    file_operation(write_file, temp_filename, 'w', ["This is a test line.\n",
                                                    "This is a duplicate test line.\n",
                                                    "This is a test line.\n",  # Duplicate line
                                                    "This is another test line.\n"])

    remove_duplicates_from_file(temp_filename)
    lines = file_operation(read_file, temp_filename)

    if lines is None or len(lines) != 3 or lines.count("This is a test line.\n") != 1:
        messagebox.showerror("Verification", "Verification Failed: There seems to be an issue with the program's functionality.")
        return

    os.remove(temp_filename)
    messagebox.showinfo("Verification", "Verification Complete: The program is functioning correctly!")

def main():
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