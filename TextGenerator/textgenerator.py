import warnings
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import gc
import tkinter as tk
from tkinter import filedialog

warnings.filterwarnings("ignore")

class InfernoLM:
    def __init__(self, device="cpu", precision="float32", model_path=None):
        self.device = device
        self.precision = precision
        self.model_path = model_path
        torch.cuda.empty_cache()
        gc.collect()
        self.tokenizer, self.model = self._load_model_and_tokenizer()

    def _load_model_and_tokenizer(self):
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
            model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True)
            model.config.do_sample = True
            model.config.temperature = 1.0
            model.config.top_p = 0.9
            model.config.top_k = 50
            model.save_pretrained(self.model_path)
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            model.to(device=self.device, dtype=torch.float16 if self.precision=="float16" else torch.float32)
            return tokenizer, model
        except Exception as e:
            raise ValueError(f"An error occurred while loading the model: {str(e)}")

    def infer_text(self, prompt, max_length=100, temperature=0.7, top_p=0.9):
        try:
            inputs = self.tokenizer(prompt, return_tensors='pt', padding=True, truncation=True, max_length=max_length).to(self.device)
            generation_config = {
                'input_ids': inputs['input_ids'],
                'max_length': max_length,
                'temperature': temperature,
                'attention_mask': inputs['attention_mask'],
                'do_sample': True,
                'top_p': top_p,
                'top_k': 50
            }
            outputs = self.model.generate(**generation_config)
            inferred_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return inferred_text.strip()
        except Exception as e:
            raise ValueError(f"An error occurred during text inferencing: {str(e)}")

def select_path():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select the directory containing model and tokenizer files")
    return folder_selected

def display_menu():
    print("\nInfernoLM: The Language Model Inferencer\n")
    print("1. Infer Text")
    print("2. Switch Model")
    print("3. Exit")

def main():
    print("Welcome to InfernoLM: The Language Model Inferencer!")
    model_path = select_path()
    if not model_path:
        print("No directory selected. Exiting.")
        return
    while True:
        try:
            device_choice = input("\nSelect the device (cpu/cuda:0): ")
            if device_choice == "cuda:0":
                precision = input("Select the precision (float32 or float16): ")
            else:
                precision = "float32"
            inferencer = InfernoLM(device=device_choice, precision=precision, model_path=model_path)
            while True:
                display_menu()
                choice = input("Enter your choice (1, 2, or 3): ")
                if choice == "1":
                    prompt = input("\nEnter your prompt: ")
                    max_length = int(input("Define the maximum length (e.g., 100): "))
                    temperature = float(input("Set the temperature (e.g., 0.7): "))
                    inferred_text = inferencer.infer_text(prompt, max_length, temperature)
                    print("\nInferred Text:")
                    print(inferred_text)
                elif choice == "2":
                    model_path = select_path()
                    if not model_path:
                        print("No directory selected. Retaining the current model.")
                        continue
                    del inferencer
                    torch.cuda.empty_cache()
                    inferencer = InfernoLM(device=device_choice, precision=precision, model_path=model_path)
                elif choice == "3":
                    print("\nThank you for using InfernoLM. Farewell!")
                    break
                else:
                    print("\nInvalid selection. Please enter 1, 2, or 3.")
        except ValueError as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
