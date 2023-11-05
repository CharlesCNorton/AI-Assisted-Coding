import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Label, Entry, Button, SUNKEN
import random
import os

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
    "ORDER_UNCHANGED": "Warning: After shuffling, the order appears unchanged. Please try again."
}


class DataMingle:
    def __init__(self, master):
        """Initialize the main application window."""
        self.master = master
        self.master.title("DataMingle: Text Scrambler for AI Training")

        self.input_file_var = tk.StringVar()
        self.output_file_var = tk.StringVar()

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
        file_frame = tk.Frame(self.master)
        file_frame.pack(pady=20)

        for idx, name in enumerate(["Input File:", "Output File:"]):
            Label(file_frame, text=name).grid(row=idx, column=0, sticky="w", padx=5, pady=5)
            Entry(file_frame, textvariable=(self.input_file_var if idx == 0 else self.output_file_var), width=50).grid(row=idx, column=1, padx=5, pady=5)

    def build_shuffle_button(self):
        """Create the 'Shuffle and Save' button."""
        Button(self.master, text="Shuffle and Save", command=self.shuffle_and_save).pack(pady=20)

    def build_status_bar(self):
        """Create the status bar at the bottom of the window."""
        self.status = tk.StringVar(value=STATUS_MSG["READY"])
        Label(self.master, textvariable=self.status, bd=1, relief=SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    def select_input_file(self):
        """Select the input text file."""
        self.set_file_path(self.input_file_var, "Select the input text file")

    def select_output_path(self):
        """Select the output path for the shuffled file."""
        self.set_file_path(self.output_file_var, "Select the output path", save=True)

    def set_file_path(self, var, title, save=False):
        """Open a dialog to select a file and set its path."""
        file_path = (filedialog.asksaveasfilename if save else filedialog.askopenfilename)(title=title, filetypes=[("Text files", "*.txt")], defaultextension=".txt")
        if file_path:
            var.set(file_path)

    def clear_paths(self):
        """Clear the selected input and output file paths."""
        self.input_file_var.set("")
        self.output_file_var.set("")
        self.status.set(STATUS_MSG["PATHS_CLEARED"])

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

        self.status.set(STATUS_MSG["PROCESSING"])
        try:
            with open(input_file, 'r') as file:
                lines = [line for line in file]
            if not lines:
                self.status.set(STATUS_MSG["EMPTY_INPUT"])
                return

            random.shuffle(lines)
            while lines[0] == lines[-1]:
                random.shuffle(lines)

            with open(output_file, 'w') as file:
                file.writelines(lines)

            self.status.set(f"Done! Shuffled data saved to {output_file}")
        except Exception as e:
            self.status.set("Error encountered.")
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DataMingle(root)
    root.mainloop()
