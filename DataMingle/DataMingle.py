import tkinter as tk
from tkinter import filedialog, messagebox
import random
import time
import numpy as np
import os

class DataMingle:
    def __init__(self, master):
        self.master = master
        self.master.title("DataMingle: Text Scrambler for AI Training")

        self.input_file_var = tk.StringVar()
        self.output_file_var = tk.StringVar()

        self.build_menu()

        self.build_input_display()

        self.build_output_display()

        self.build_shuffle_button()

        self.build_status_bar()

    def build_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Input File", command=self.select_input_file)
        file_menu.add_command(label="Select Output Path", command=self.select_output_path)
        file_menu.add_command(label="Clear Paths", command=self.clear_paths)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

    def build_input_display(self):
        input_label = tk.Label(self.master, text="Input File:")
        input_label.pack(pady=20)

        input_display = tk.Entry(self.master, textvariable=self.input_file_var, width=50)
        input_display.pack(pady=5)

    def build_output_display(self):
        output_label = tk.Label(self.master, text="Output File:")
        output_label.pack(pady=20)

        output_display = tk.Entry(self.master, textvariable=self.output_file_var, width=50)
        output_display.pack(pady=5)

    def build_shuffle_button(self):
        shuffle_button = tk.Button(self.master, text="Shuffle and Save", command=self.shuffle_and_save)
        shuffle_button.pack(pady=20)

    def build_status_bar(self):
        self.status = tk.StringVar()
        self.status.set("Ready.")
        status_bar = tk.Label(self.master, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
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
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()

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

            original_first_line = lines[0]

            seed_value = int(time.time()) ^ int.from_bytes(os.urandom(16), byteorder='big')
            random.seed(seed_value)

            for _ in range(5):
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