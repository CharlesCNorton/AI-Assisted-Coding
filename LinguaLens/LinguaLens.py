import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar, Toplevel
from collections import defaultdict

def categorize_length(sentence):
    words = len(sentence.split())
    if 1 <= words <= 5:
        return "Short"
    elif 6 <= words <= 15:
        return "Medium"
    elif 16 <= words <= 50:
        return "Large"
    else:
        return "Other"

def categorize_ending(sentence):
    if sentence.endswith("?"):
        return "Question"
    elif sentence.endswith("."):
        return "Statement"
    elif sentence.endswith("!"):
        return "Exclamation"
    else:
        return "Other"

def analyze_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        data = defaultdict(lambda: defaultdict(int))
        total_sentences = 0

        for line in lines:
            line = line.strip()
            length_cat = categorize_length(line)
            ending_cat = categorize_ending(line)
            data[length_cat][ending_cat] += 1
            total_sentences += 1

        summary = f"Analysis of '{file_path.split('/')[-1]}':\nTotal Sentences: {total_sentences:,.0f}\n" + "-"*40 + "\n"
        results.delete(1.0, tk.END)
        results.insert(tk.END, summary)

        for length in ["Large", "Medium", "Short", "Other"]:
            if length in data:
                results.insert(tk.END, f"{length} Sentences:\n")
                for ending, count in data[length].items():
                    results.insert(tk.END, f" - {ending}: {count:,.0f}\n")
                results.insert(tk.END, "\n")

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_files():
    filename = filedialog.askopenfilename(filetypes =[("Text files", "*.txt")])
    if filename:
        analyze_file(filename)

def show_help():
    help_window = Toplevel(root)
    help_window.title("Help")
    help_text = """LinguaLens - Dataset Examination Tool

1. Browse to select a text file for analysis.
2. The application categorizes sentences into:
   - Short (1-5 words)
   - Medium (6-15 words)
   - Large (16-50 words)
   - Other (for longer sentences)

3. It also classifies endings as Questions, Statements, or Exclamations.

This tool helps to analyze the symmetry of datasets intended for language model fine-tuning."""
    label = tk.Label(help_window, text=help_text, padx=10, pady=10, justify=tk.LEFT)
    label.pack()

root = tk.Tk()
root.title("LinguaLens")
root.geometry("500x500")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open...", command=browse_files)
file_menu.add_command(label="Exit", command=root.quit)

help_menu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_help)

results = Text(root, wrap=tk.WORD, height=24, width=60)
results.pack(padx=10, pady=10)

scroll = Scrollbar(root, command=results.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

results.configure(yscrollcommand=scroll.set)

root.mainloop()
