import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Label, Entry, Button, SUNKEN
import random
import time
import os

class DataMingle:
    def __init__(self, master):
        self.master = master
        self.master.title("DataMingle: Text Scrambler for AI Training")

        self.input_file_var = tk.StringVar()
        self.output_file_var = tk.StringVar()

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
        """Build the input and output file displays."""
        file_frame = tk.Frame(self.master)
        file_frame.pack(pady=20)

        input_label = Label(file_frame, text="Input File:")
        input_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        input_display = Entry(file_frame, textvariable=self.input_file_var, width=50)
        input_display.grid(row=0, column=1, padx=5, pady=5)

        output_label = Label(file_frame, text="Output File:")
        output_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        output_display = Entry(file_frame, textvariable=self.output_file_var, width=50)
        output_display.grid(row=1, column=1, padx=5, pady=5)

    def build_shuffle_button(self):
        """Build the shuffle button."""
        shuffle_button = Button(self.master, text="Shuffle and Save", command=self.shuffle_and_save)
        shuffle_button.pack(pady=20)

    def build_status_bar(self):
        """Build the status bar at the bottom."""
        self.status = tk.StringVar()
        self.status.set("Ready.")
        status_bar = Label(self.master, textvariable=self.status, bd=1, relief=SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(title="Select the input text file", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.input_file_var.set(file_path)

    def select_output_path(self):
        file_path = filedialog.asksaveasfilename(title="Select the output path", filetypes=[("Text files", "*.txt")], defaultextension=".txt")
        if file_path:
            self.output_file_var.set(file_path)

    def clear_paths(self):
        self.input_file_var.set("")
        self.output_file_var.set("")
        self.status.set("Paths cleared.")

    def shuffle_and_save(self):
        """Shuffle lines from the input file and save them to the output file."""
        input_file = self.input_file_var.get().strip()
        output_file = self.output_file_var.get().strip()

        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist!")
            return

        if not input_file:
            messagebox.showerror("Error", "Please select an input file!")
            return

        if not output_file:
            messagebox.showerror("Error", "Please select an output file!")
            return

        self.status.set("Processing...")
        try:
            with open(input_file, 'r') as file:
                lines = file.readlines()

            # Ensure that there are lines to shuffle
            if not lines:
                self.status.set("The input file is empty.")
                return

            original_first_line = lines[0]
            random.shuffle(lines)

            if lines[0] == original_first_line:
                self.status.set("Warning: After shuffling, the order appears unchanged. Please try again.")
                return

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