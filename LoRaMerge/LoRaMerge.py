import os
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

def display_menu(trust_remote_code):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("========= LoraMerge: Merge PEFT Adapters with a Base Model =========")
    print("\nOptions:")
    print("1. Merge models")
    print("2. Acknowledgment & Citation")
    print("3. Toggle Trust Remote Code (Currently: {})".format(trust_remote_code))
    print("4. Exit")
    choice = input("\nEnter your choice: ")
    return choice

def display_acknowledgment():
    print("\nAcknowledgment & Citation:")
    print("\nLoraMerge is based on an original script by TheBloke available as a Gist at:")
    print("https://gist.github.com/TheBloke/d31d289d3198c24e0ca68aaf37a19032")
    print("\nWe deeply appreciate the foundational work by TheBloke and aim to extend its usability with this tool.")

def get_args():
    parser = argparse.ArgumentParser(description="Merge PEFT Adapters with a Base Model.")
    parser.add_argument("--device", type=str, default="auto", help="Device for model loading, e.g. 'cuda:0', 'cpu'. 'auto' to auto-select.")
    return parser.parse_args()

def select_directory(title="Select a directory"):
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title=title)
    if not folder_selected:
        messagebox.showerror("Error", f"{title} cancelled or failed. Exiting.")
        exit()
    return folder_selected

def merge_models(args, trust_remote_code):
    base_model_name_or_path = select_directory("Select pretrained directory for base model")
    peft_model_path = select_directory("Select pretrained directory for PEFT model")
    output_dir = select_directory("Select directory to save the model")
    device_arg = {'device_map': 'auto'} if args.device == 'auto' else {'device_map': {"": args.device}}
    print(f"Loading base model: {base_model_name_or_path}")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name_or_path,
        return_dict=True,
        torch_dtype=torch.float16,
        trust_remote_code=trust_remote_code,
        **device_arg
    )
    print(f"Loading PEFT: {peft_model_path}")
    model = PeftModel.from_pretrained(base_model, peft_model_path, **device_arg)
    print("Running merge_and_unload")
    model = model.merge_and_unload()
    tokenizer = AutoTokenizer.from_pretrained(base_model_name_or_path)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model saved to {output_dir}")

def main():
    args = get_args()
    trust_remote_code = False
    while True:
        choice = display_menu(trust_remote_code)
        if choice == '1':
            merge_models(args, trust_remote_code)
            input("\nPress Enter to continue...")
        elif choice == '2':
            display_acknowledgment()
            input("\nPress Enter to continue...")
        elif choice == '3':
            trust_remote_code = not trust_remote_code
        elif choice == '4':
            break
        else:
            input("Invalid choice. Press Enter to continue...")

if __name__ == "__main__":
    main()
