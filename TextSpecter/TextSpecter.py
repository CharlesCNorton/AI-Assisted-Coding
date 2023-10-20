import string
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter

COMMON_WORDS = set(["and", "to", "the", "of", "in", "is", "on", "for", "with", "as", "it", "at", "by", "an", "be", "or", "we",
                    "you", "not", "from", "but", "are", "they", "he", "she", "we", "I", "this", "that", "have", "do", "was",
                    "can", "will", "my", "your", "his", "her", "its", "our", "their", "there", "when", "where", "how", "why",
                    "which", "who", "whom", "me", "us", "them"])

def select_file():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        return file_path
    except Exception as e:
        messagebox.showerror("Error", f"Error while selecting the file: {e}")
        return None

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def categorize_characters(text):
    char_freq = Counter(text)

    common_chars = set(string.ascii_letters + string.digits + string.punctuation)
    whitespace_chars = set(string.whitespace)
    diacritics_chars = set("áéíóúýÁÉÍÓÚÝäëïöüÿÄËÏÖÜàèìòùÀÈÌÒÙãñõÃÑÕâêîôûÂÊÎÔÛçÇ")
    currency_chars = set("¢£¤¥€₹₽₺₩$")
    uncommon_chars = set(char_freq.keys()) - common_chars - whitespace_chars - diacritics_chars - currency_chars
    unicode_punctuations = set(char for char in char_freq.keys() if char in string.punctuation and char not in common_chars)

    return {
        "standard": common_chars,
        "whitespace": whitespace_chars,
        "diacritics": diacritics_chars,
        "currency": currency_chars,
        "uncommon": uncommon_chars,
        "unicode punctuations": unicode_punctuations,
        "frequencies": char_freq
    }

def count_common_words(text):
    word_freq = Counter(text.lower().split())
    return {word: word_freq[word] for word in COMMON_WORDS if word in word_freq}

def summarize_characters(filename):
    text = read_file(filename)
    if text is None:
        return

    categories = categorize_characters(text)
    freq = categories["frequencies"]

    print(f"\nSummary for '{filename}':")
    print(f"\nTotal characters: {len(text)}")
    print(f"Unique characters: {len(freq)}")

    for cat, chars in categories.items():
        if cat != "frequencies":
            count = sum(freq[char] for char in chars if char in freq)
            if count:
                print(f"\n{cat.title()} characters (total {count}):")
                for char in sorted(chars):
                    if char in freq:
                        print(f"'{char}' : {freq[char]}")

    threshold = 0.01 * len(text)
    infrequent_chars = {char: count for char, count in freq.items() if count < threshold}
    if infrequent_chars:
        print("\nInfrequent characters:")
        for char, count in sorted(infrequent_chars.items(), key=lambda x: x[1]):
            print(f"'{char}' : {count}")

    common_word_counts = count_common_words(text)
    if common_word_counts:
        print("\nCommon word counts:")
        for word, count in sorted(common_word_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{word} : {count}")

def main():
    file_path = select_file()
    if file_path:
        summarize_characters(file_path)
    else:
        print("No file selected.")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
