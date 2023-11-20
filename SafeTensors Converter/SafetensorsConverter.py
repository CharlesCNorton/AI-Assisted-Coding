import os
import re
import torch
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from safetensors.torch import load_file, save_file

selected_directory = ""

def check_file_size(sf_filename: str, pt_filename: str):
    try:
        sf_size = os.stat(sf_filename).st_size
        pt_size = os.stat(pt_filename).st_size
        if (sf_size - pt_size) / pt_size > 0.01:
            raise RuntimeError(
                f"The file size difference is more than 1%:\n - {sf_filename}: {sf_size}\n - {pt_filename}: {pt_size}"
            )
    except Exception as e:
        messagebox.showerror("File Size Check Error", str(e))
        return False
    return True

def convert_file(pt_filename: str, sf_filename: str):
    try:
        if os.path.exists(sf_filename):
            if not messagebox.askyesno("File Exists", f"The file {sf_filename} already exists. Do you want to overwrite it?"):
                return
        loaded = torch.load(pt_filename, map_location="cpu")
        if "state_dict" in loaded:
            loaded = loaded["state_dict"]
        loaded = {k: v.contiguous() for k, v in loaded.items()}
        os.makedirs(os.path.dirname(sf_filename), exist_ok=True)
        save_file(loaded, sf_filename, metadata={"format": "pt"})
        if check_file_size(sf_filename, pt_filename):
            reloaded = load_file(sf_filename)
            for k in loaded:
                pt_tensor = loaded[k]
                sf_tensor = reloaded[k]
                if not torch.equal(pt_tensor, sf_tensor):
                    raise RuntimeError(f"The output tensors do not match for key {k}")
    except Exception as e:
        messagebox.showerror("Conversion Error", str(e))

def convert_all_files_in_directory(directory: str):
    try:
        for filename in os.listdir(directory):
            pt_filename = os.path.join(directory, filename)
            sf_filename = None

            match = re.match(r"pytorch_model-(\d+)-of-(\d+).bin", filename)
            if match:
                part_num, total_parts = match.groups()
                sf_filename = os.path.join(directory, f"model-{part_num.zfill(5)}-of-{total_parts.zfill(5)}.safetensors")

            elif filename == "pytorch_model.bin":
                sf_filename = os.path.join(directory, "model.safetensors")

            if sf_filename:
                convert_file(pt_filename, sf_filename)
    except Exception as e:
        messagebox.showerror("Directory Conversion Error", str(e))

def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        directory_label.config(text=f"Selected Directory: {selected_directory}")

def start_conversion():
    if selected_directory:
        try:
            convert_all_files_in_directory(selected_directory)
            messagebox.showinfo("Success", "Files converted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("No Directory Selected", "Please select a directory first.")

def main():
    global directory_label

    root = tk.Tk()
    root.title("Bin to SafeTensors Converter")

    frame = ttk.Frame(root, padding="30")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    title_label = ttk.Label(frame, text="Bin to SafeTensors Converter", font=("Arial", 16))
    title_label.grid(row=0, column=0, pady=20, sticky=tk.W)

    directory_label = ttk.Label(frame, text="Selected Directory: None", font=("Arial", 12))
    directory_label.grid(row=1, column=0, pady=10, sticky=tk.W)

    select_button = ttk.Button(frame, text="Select Directory", command=select_directory)
    select_button.grid(row=2, column=0, pady=10)

    convert_button = ttk.Button(frame, text="Convert", command=start_conversion)
    convert_button.grid(row=3, column=0, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
