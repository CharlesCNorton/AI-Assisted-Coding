import os
import tkinter as tk
from tkinter import filedialog, simpledialog
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig, BitsAndBytesConfig

def select_directory(title="Select Directory"):
    """Open a dialog to select a directory."""
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title=title)
    return path

def select_text_file(title="Select Text File"):
    """Open a dialog to select a text file."""
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(title=title, filetypes=[("Text files", "*.txt")])
    with open(filepath, 'r') as f:
        content = f.readlines()
    return content

def main():
    while True:
        print("\nQuantization Menu:")
        print("1. GPTQ Quantization - Quantize a model with the GPTQ method.")
        print("2. 8-bit Quantization using bitsandbytes - Convert a model to 8-bit precision.")
        print("3. 4-bit Quantization using bitsandbytes - Convert a model to 4-bit precision.")
        print("4. Advanced 4-bit using NF4 data type - Use the NF4 data type for 4-bit quantization.")
        print("5. Nested Quantization for memory efficiency - Save more memory using nested quantization.")
        print("6. Exit")
        choice = input("\nEnter your choice: ")

        try:
            if choice == '1':
                model_path = select_directory(title="Select Model Directory")
                dataset_choice = input("Do you have a custom dataset in a text file? (yes/no): ")
                if dataset_choice.lower() == 'yes':
                    dataset = select_text_file(title="Select Dataset Text File")
                else:
                    dataset = "c4"
                tokenizer = AutoTokenizer.from_pretrained(model_path)
                gptq_config = GPTQConfig(bits=4, dataset=dataset, tokenizer=tokenizer)
                model = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=gptq_config)
                output_path = select_directory(title="Select Output Directory for Quantized Model")
                model.save_pretrained(output_path)

            elif choice == '2':
                model_path = select_directory(title="Select Model Directory")
                model_8bit = AutoModelForCausalLM.from_pretrained(model_path, load_in_8bit=True)
                output_path = select_directory(title="Select Output Directory for Quantized Model")
                model_8bit.save_pretrained(output_path)

            elif choice == '3':
                model_path = select_directory(title="Select Model Directory")
                model_4bit = AutoModelForCausalLM.from_pretrained(model_path, load_in_4bit=True)
                output_path = select_directory(title="Select Output Directory for Quantized Model")
                model_4bit.save_pretrained(output_path)

            elif choice == '4':
                model_path = select_directory(title="Select Model Directory")
                quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)
                model_nf4 = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=quantization_config)
                output_path = select_directory(title="Select Output Directory for Quantized Model")
                model_nf4.save_pretrained(output_path)

            elif choice == '5':
                model_path = select_directory(title="Select Model Directory")
                double_quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_use_double_quant=True)
                model_double_quant = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=double_quant_config)
                output_path = select_directory(title="Select Output Directory for Quantized Model")
                model_double_quant.save_pretrained(output_path)

            elif choice == '6':
                break

            else:
                print("Invalid choice. Please choose a valid option.")

        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
