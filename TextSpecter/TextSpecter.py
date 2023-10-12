import string
import tkinter as tk
from tkinter import filedialog
from collections import Counter

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return file_path

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def categorize_characters(text):
    char_freq = Counter(text)

    common_chars = set(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
    whitespace_chars = set(string.whitespace)
    diacritics_chars = set("áéíóúýÁÉÍÓÚÝäëïöüÿÄËÏÖÜàèìòùÀÈÌÒÙãñõÃÑÕâêîôûÂÊÎÔÛçÇ")
    currency_chars = set("¢£¤¥€₹₽₺₩$")

    standard_chars = common_chars - whitespace_chars
    uncommon_chars = set(char_freq.keys()) - common_chars - diacritics_chars - currency_chars
    unicode_punctuations = set(char for char in char_freq.keys() if char in string.punctuation and char not in common_chars)

    return {
        "standard": standard_chars,
        "whitespace": whitespace_chars,
        "diacritics": diacritics_chars,
        "currency": currency_chars,
        "uncommon": uncommon_chars,
        "unicode_punctuations": unicode_punctuations,
        "frequencies": char_freq
    }

def summarize_characters(filename):
    text = read_file(filename)
    if text is None:
        return

    categories = categorize_characters(text)

    print(f"Total characters in '{filename}':", len(text))
    print("Unique characters:", len(categories["frequencies"]))

    for cat, chars in categories.items():
        if cat != "frequencies":
            count = sum(categories["frequencies"][char] for char in chars if char in categories["frequencies"])
            if count:
                print(f"\n{cat.replace('_', ' ').title()} characters (total {count}):")
                for char in chars:
                    if char in categories["frequencies"]:
                        print(f"'{char}' : {categories['frequencies'][char]}")

    threshold = 0.01 * len(text)
    odd_chars = {char: count for char, count in categories["frequencies"].items() if count < threshold}
    if odd_chars:
        print("\nOdd characters:")
        for char, count in odd_chars.items():
            print(f"'{char}' : {count}")

if __name__ == "__main__":
    file_path = select_file()
    if file_path:
        summarize_characters(file_path)
    else:
        print("No file selected.")
