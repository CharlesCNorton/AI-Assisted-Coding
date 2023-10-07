import tkinter as tk
from tkinter import filedialog, simpledialog
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig
import torch

def select_path(prompt="Select Directory"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    path = filedialog.askdirectory(title=prompt)  # Show the directory dialog
    return path

def get_bit_choice():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    while True:
        choice = simpledialog.askstring("Input", "Choose the bit size for quantization (2, 4, 8):")
        if choice in ['2', '4', '8']:
            return int(choice)
        else:
            print("Invalid bit size. Please choose 2, 4, or 8.")

def main():
    bit_choice = get_bit_choice()

    while True:
        print("\nQuantization Menu:")
        print("1. GPTQ Quantization")
        print("2. Exit")
        choice = input("\nEnter your choice: ")

        if choice == '1':
            print(f"Selected {bit_choice}-bit quantization.")
            print("Loading model...")
            model_path = select_path("Select Model to Quantize")
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            gptq_config = GPTQConfig(bits=bit_choice, dataset="c4", tokenizer=tokenizer)

            # Determine save path before quantizing
            save_path = select_path("Select Directory to Save Quantized Model")

            print("Starting GPTQ quantization...")
            model = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=gptq_config).to("cuda")

            # This ensures any backend requirements are met
            model.disable_exllama = True

            # Saving the quantized model
            print(f"Saving quantized model to {save_path}")
            model.save_pretrained(save_path)
            print("GPTQ quantization complete!")

            # Cleaning up
            del model
            torch.cuda.empty_cache()

        elif choice == '2':
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
