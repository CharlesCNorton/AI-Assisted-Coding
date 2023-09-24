import tkinter as tk
from tkinter import filedialog

def remove_duplicates_from_file(filename):
    unique_lines = []
    seen_lines = set()

    try:
        with open(filename, 'r') as f:
            for line in f:
                if line not in seen_lines:
                    unique_lines.append(line)
                    seen_lines.add(line)

        with open(filename, 'w') as f:
            for line in unique_lines:
                f.write(line)

        print(f"Successfully removed duplicates from {filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    root = tk.Tk()
    root.withdraw()
    while True:
        print("1. Remove duplicates from a file")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            filename = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text files", "*.txt")])
            if filename:
                remove_duplicates_from_file(filename)
            else:
                print("No file selected. Please try again.")
        elif choice == '2':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
