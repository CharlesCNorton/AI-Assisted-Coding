import os
import tkinter as tk
from tkinter import filedialog
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig
import torch
import traceback

def select_path(prompt="Select Directory"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    path = filedialog.askdirectory(title=prompt)  # Show the directory dialog
    return path

def check_model_saved(directory):
    return any([file.endswith(".bin") for file in os.listdir(directory)])

def print_divider():
    print("-" * 50)

def main():
    while True:
        print_divider()
        print("\nGPTQ Quantization Menu:".center(50))
        print_divider()
        print("1. GPTQ Quantization")
        print("2. Set Quantization Bits (Current: 4)")
        print("3. Exit")
        print_divider()

        choice = input("\nEnter your choice: ")

        try:
            if choice == '1':
                print("\n[INFO] Loading model...")
                model_path = select_path("Select Model to Quantize")

                print("[INFO] Loading tokenizer...")
                tokenizer = AutoTokenizer.from_pretrained(model_path)

                bits = 4
                gptq_config = GPTQConfig(bits=bits, dataset="c4", tokenizer=tokenizer)

                save_path = select_path("Select Directory to Save Quantized Model")

                print("[INFO] Starting GPTQ quantization...")

                model = AutoModelForCausalLM.from_pretrained(model_path, quantization_config=gptq_config, device_map='cuda')

                model.disable_exllama = True

                print(f"[INFO] Saving quantized model to {save_path}...")
                model.save_pretrained(save_path)

                # Check if model was actually saved
                if check_model_saved(save_path):
                    print("[SUCCESS] Model saved successfully!")
                else:
                    print("[ERROR] Model not found in the specified directory after quantization!")

                # Cleanup
                print("[INFO] Cleaning up resources...")
                del model
                torch.cuda.empty_cache()
                print("[INFO] Cleanup complete.")

            elif choice == '2':
                print("\nSet Quantization Bits:")
                print("a. 2-bit")
                print("b. 4-bit (Default)")
                print("c. 8-bit")
                bit_choice = input("\nSelect bit option (a/b/c): ")

                if bit_choice == 'a':
                    bits = 2
                elif bit_choice == 'b':
                    bits = 4
                elif bit_choice == 'c':
                    bits = 8
                else:
                    print("[ERROR] Invalid bit selection.")
                print(f"[INFO] Quantization bits set to {bits}-bit.")

            elif choice == '3':
                print("[INFO] Exiting program.")
                break

            else:
                print("[ERROR] Invalid choice. Please choose a valid option.")

        except Exception as e:
            print("[ERROR] An unexpected error occurred during the process.")
            print(f"[DETAILS] {e}")
            print("[TRACEBACK] Below is the detailed traceback:")
            traceback.print_exc()

if __name__ == "__main__":
    main()
