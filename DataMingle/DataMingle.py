import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Label, Entry, Button, Frame, StringVar
import random
import os
from threading import Thread

ERROR_MSG = {
    "SELECT_INPUT": "Please select an input file!",
    "INPUT_NOT_EXIST": "Input file does not exist!",
    "SELECT_OUTPUT": "Please select an output file!"
}

STATUS_MSG = {
    "READY": "Ready.",
    "PATHS_CLEARED": "Paths cleared.",
    "PROCESSING": "Processing...",
    "EMPTY_INPUT": "The input file is empty.",
    "ORDER_UNCHANGED": "Order appears unchanged after shuffling. Please try again.",
    "DONE": "Done! Shuffled data saved to: {}",
    "ERROR": "Error encountered: {}"
}

FILE_TYPES = [("Text files", "*.txt")]
DEFAULT_EXTENSION = ".txt"

class DataMingleApp:
    def __init__(self, master):
        """Initialize the main application window."""
        self.master = master
        self.master.title("DataMingle: Text Scrambler for AI Training")

        self.input_file_var = StringVar()
        self.output_file_var = StringVar()
        self.status_var = StringVar(value=STATUS_MSG["READY"])

        self.build_ui()

    def build_ui(self):
        """Build the main user interface components."""
        self.build_menu()
        self.build_file_displays()
        self.build_shuffle_button()
        self.build_status_bar()

    def build_menu(self):
        """Build the main menu."""
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Input File", command=self.select_input_file)
        file_menu.add_command(label="Select Output Path", command=self.select_output_path)
        file_menu.add_command(label="Clear Paths", command=self.clear_paths)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

    def build_file_displays(self):
        """Display the input and output file paths."""
        file_frame = Frame(self.master)
        file_frame.pack(pady=20)

        Label(file_frame, text="Input File:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        Entry(file_frame, textvariable=self.input_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)

        Label(file_frame, text="Output File:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        Entry(file_frame, textvariable=self.output_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)

    def build_shuffle_button(self):
        """Create the 'Shuffle and Save' button."""
        Button(self.master, text="Shuffle and Save", command=self.start_shuffle_and_save).pack(pady=20)

    def build_status_bar(self):
        """Create the status bar at the bottom of the window."""
        Label(self.master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    def select_input_file(self):
        """Select the input text file."""
        self.set_file_path(self.input_file_var, "Select the input text file")

    def select_output_path(self):
        """Select the output path for the shuffled file."""
        self.set_file_path(self.output_file_var, "Select the output path", save=True)

    def set_file_path(self, var, title, save=False):
        """Open a dialog to select a file and set its path."""
        options = {
            'title': title,
            'filetypes': FILE_TYPES,
            'defaultextension': DEFAULT_EXTENSION
        }
        file_path = filedialog.asksaveasfilename(**options) if save else filedialog.askopenfilename(**options)
        if file_path:
            var.set(file_path)

    def clear_paths(self):
        """Clear the selected input and output file paths."""
        self.input_file_var.set("")
        self.output_file_var.set("")
        self.status_var.set(STATUS_MSG["PATHS_CLEARED"])

    def start_shuffle_and_save(self):
        """Start the shuffle and save operation in a separate thread to keep UI responsive."""
        Thread(target=self.shuffle_and_save, daemon=True).start()

    def shuffle_and_save(self):
        """Shuffle the lines of the input file and save it to the output path."""
        input_file = self.input_file_var.get().strip()
        output_file = self.output_file_var.get().strip()

        if not input_file:
            messagebox.showerror("Error", ERROR_MSG["SELECT_INPUT"])
            return

        if not os.path.exists(input_file):
            messagebox.showerror("Error", ERROR_MSG["INPUT_NOT_EXIST"])
            return

        if not output_file:
            messagebox.showerror("Error", ERROR_MSG["SELECT_OUTPUT"])
            return

        self.status_var.set(STATUS_MSG["PROCESSING"])
        try:
            with open(input_file, 'r') as file:
                lines = file.readlines()

            if not lines:
                self.status_var.set(STATUS_MSG["EMPTY_INPUT"])
                return

            shuffled = False
            while not shuffled:
                before_shuffle = lines.copy()
                random.shuffle(lines)
                shuffled = any(before != after for before, after in zip(before_shuffle, lines))

            with open(output_file, 'w') as file:
                file.writelines(lines)

            self.status_var.set(STATUS_MSG["DONE"].format(output_file))
        except Exception as e:
            self.status_var.set(STATUS_MSG["ERROR"].format(e))
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DataMingleApp(root)
    root.mainloop()
