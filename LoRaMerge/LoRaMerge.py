import os
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Refactoring color codes into a dictionary
colors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKCYAN': '\033[96m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}

def clear_screen():
    """ Clear the terminal screen. """
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """ Display the terminal menu. """
    clear_screen()
    print(colors['OKGREEN'] + colors['BOLD'] + "========= LoraMerge: Merge PEFT Adapters with a Base Model =========" + colors['ENDC'])
    print(colors['OKBLUE'] + "\nAn homage to the legendary work by TheBloke:" + colors['ENDC'])
    print(colors['OKCYAN'] + "https://gist.github.com/TheBloke/d31d289d3198c24e0ca68aaf37a19032" + colors['ENDC'])
    print(colors['HEADER'] + "\nOptions:" + colors['ENDC'])
    print("1. " + colors['OKBLUE'] + "Merge models" + colors['ENDC'])
    print("2. " + colors['OKBLUE'] + "Dedication & Profound Acknowledgment to TheBloke" + colors['ENDC'])
    print("3. " + colors['OKBLUE'] + "Exit" + colors['ENDC'])
    return input(colors['OKGREEN'] + colors['BOLD'] + "\nEnter your choice: " + colors['ENDC'])

def display_acknowledgment():
    """ A heartfelt and reverential acknowledgment for TheBloke. """
    print(colors['HEADER'] + "\nDedication & Profound Acknowledgment:" + colors['ENDC'])
    print(colors['OKBLUE'] + "\nLoraMerge, while a humble tool, stands on the shoulders of a giant..." + colors['ENDC'])
    # Rest of the function remains the same...

def parse_arguments():
    """ Parse command line arguments with enhanced details and validation. """
    parser = argparse.ArgumentParser(description="Merge PEFT Adapters with a Base Model.")
    parser.add_argument("--device", type=str, default="auto", choices=['cuda:0', 'cpu', 'auto'], help="Device for model loading (cuda:0, cpu, auto). Default: auto.")
    return parser.parse_args()

def select_directory(title):
    """ GUI based directory selection. """
    try:
        root = tk.Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory(title=title)
        if not folder_selected:
            raise Exception("Directory selection cancelled or failed.")
        return folder_selected
    except Exception as e:
        messagebox.showerror("Error", f"{title} failed: {e}")
        raise

def merge_models(args):
    """
    The core functionality for merging PEFT Adapters with a Base Model.
    """
    try:
        base_model_name_or_path = select_directory("Select pretrained directory for base model")
        peft_model_path = select_directory("Select pretrained directory for PEFT model")
        output_dir = select_directory("Select directory to save the model")

        device_arg = {'device_map': 'auto'} if args.device == 'auto' else {'device_map': {"": args.device}}

        print(f"Loading base model: {base_model_name_or_path}")
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name_or_path,
            return_dict=True,
            torch_dtype=torch.float16,
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

    except Exception as e:
        print(f"An error occurred: {e}")
        return

def main():
    args = parse_arguments()

    while True:
        choice = display_menu()

        if choice == '1':
            merge_models(args)
            input(colors['OKGREEN'] + "\nPress Enter to continue..." + colors['ENDC'])
        elif choice == '2':
            display_acknowledgment()
            input(colors['OKGREEN'] + "\nPress Enter to continue..." + colors['ENDC'])
        elif choice == '3':
            print(colors['OKBLUE'] + "Thank you for using LoraMerge! Exiting..." + colors['ENDC'])
            break
        else:
            input(colors['WARNING'] + "Invalid choice. Press Enter to return to the menu..." + colors['ENDC'])

def user_confirmation(message):
    """
    Prompt the user for a confirmation with a Yes/No option.
    """
    while True:
        choice = input(message + " (y/n): ").lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please respond with 'y' or 'n'.")

if __name__ == "__main__":
    main()
