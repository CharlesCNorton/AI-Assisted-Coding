import os
import tkinter as tk
from tkinter import filedialog
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig, BitsAndBytesConfig

def select_path(title="Select Directory"):
    """Open a dialog to select a path."""
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title=title)
    return path

def main():
    while True:
        print("\nQuantization Menu:")
        print("1. GPTQ Quantization")
        print("2. 8-bit Quantization using bitsandbytes")
        print("3. 4-bit Quantization using bitsandbytes")
        print("4. Advanced 4-bit using NF4 data type")
        print("5. Nested Quantization for memory efficiency")
        print("6. Exit")
        choice = input("\nEnter your choice: ")

        try:
            if choice == '1':
                model_path = select_path(title="Select Model Directory")
                tokenizer = AutoTokenizer.from_pretrained(model_path)
                gptq_config = GPTQConfig(bits=4, dataset="c4", tokenizer=tokenizer)
                model = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=gptq_config)
                output_path = select_path(title="Select Output Directory for Quantized Model")
                model.save_pretrained(output_path)

            elif choice == '2':
                model_path = select_path(title="Select Model Directory")
                model_8bit = AutoModelForCausalLM.from_pretrained(model_path, load_in_8bit=True)
                output_path = select_path(title="Select Output Directory for Quantized Model")
                model_8bit.save_pretrained(output_path)

            elif choice == '3':
                model_path = select_path(title="Select Model Directory")
                model_4bit = AutoModelForCausalLM.from_pretrained(model_path, load_in_4bit=True)
                output_path = select_path(title="Select Output Directory for Quantized Model")
                model_4bit.save_pretrained(output_path)

            elif choice == '4':
                model_path = select_path(title="Select Model Directory")
                quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)
                model_nf4 = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=quantization_config)
                output_path = select_path(title="Select Output Directory for Quantized Model")
                model_nf4.save_pretrained(output_path)

            elif choice == '5':
                model_path = select_path(title="Select Model Directory")
                double_quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_use_double_quant=True)
                model_double_quant = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=double_quant_config)
                output_path = select_path(title="Select Output Directory for Quantized Model")
                model_double_quant.save_pretrained(output_path)

            elif choice == '6':
                break

            else:
                print("Invalid choice. Please choose a valid option.")

        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
