import tkinter as tk
from tkinter import filedialog, messagebox, Text, Scrollbar, Toplevel
from collections import defaultdict
import logging
import re

logging.basicConfig(level=logging.INFO)

class SentenceAnalyzer:
    @staticmethod
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

    @staticmethod
    def categorize_character_length(sentence):
        length = len(sentence)
        if 1 <= length <= 50:
            return "Short"
        elif 51 <= length <= 100:
            return "Medium"
        elif 101 <= length <= 200:
            return "Long"
        else:
            return "Very Long"

    @staticmethod
    def categorize_ending(sentence):
        if sentence.endswith("?"):
            return "Question"
        elif sentence.endswith("."):
            return "Statement"
        elif sentence.endswith("!"):
            return "Exclamation"
        else:
            return "Other"

    @staticmethod
    def split_into_sentences(text):
        sentences = re.split(r'[.!?]', text)
        return filter(lambda s: s.strip(), sentences)

    @staticmethod
    def analyze_file(file_path):
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                content = file.read()

            data = defaultdict(lambda: defaultdict(int))
            total_sentences = 0

            for sentence in SentenceAnalyzer.split_into_sentences(content):
                length_cat = SentenceAnalyzer.categorize_length(sentence)
                char_length_cat = SentenceAnalyzer.categorize_character_length(sentence)
                ending_cat = SentenceAnalyzer.categorize_ending(sentence)
                data[length_cat][ending_cat] += 1
                data[char_length_cat][ending_cat] += 1
                total_sentences += 1

            return data, total_sentences

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")
            logging.error(f"File not found: {file_path}")
            return None, 0
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            logging.error(f"Error processing file: {e}")
            return None, 0

class LinguaLensApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("LinguaLens")
        self.root.geometry("600x600")

        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open...", command=self.browse_files)
        file_menu.add_command(label="Save Analysis...", command=self.save_analysis)
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_help)

        self.results = Text(self.root, wrap=tk.WORD, height=30, width=70)
        self.results.pack(padx=10, pady=10)

        scroll = Scrollbar(self.root, command=self.results.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.results.configure(yscrollcommand=scroll.set)

    def browse_files(self):
        try:
            filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if filename:
                data, total_sentences = SentenceAnalyzer.analyze_file(filename)
                self.display_results(data, total_sentences, filename)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            logging.error(f"Error in browse_files: {e}")

    def display_results(self, data, total_sentences, filename):
        if data:
            summary = f"Analysis of '{filename.split('/')[-1]}':\nTotal Sentences: {total_sentences:,.0f}\n" + "-" * 40 + "\n"
            self.results.delete(1.0, tk.END)
            self.results.insert(tk.END, summary)

            for length in ["Large", "Medium", "Short", "Other"]:
                if length in data:
                    self.results.insert(tk.END, f"{length} Sentences:\n")
                    for ending, count in data[length].items():
                        self.results.insert(tk.END, f" - {ending}: {count:,.0f}\n")
                    self.results.insert(tk.END, "\n")

    def save_analysis(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if file:
            text_to_save = self.results.get("1.0", tk.END)
            file.write(text_to_save)
            file.close()

    def show_help(self):
        help_window = Toplevel(self.root)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = LinguaLensApp(root)
    root.mainloop()
