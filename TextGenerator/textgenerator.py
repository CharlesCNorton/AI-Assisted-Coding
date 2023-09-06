import warnings
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import gc
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore, Style

init(autoreset=True)
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

    def infer_text(self, prompt, mode="full", max_length=100, temperature=0.7, top_p=0.9, real_time=False):
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

            if real_time:
                output_tokens = []
                for i in range(max_length):
                    generation_config['max_length'] = i + 1
                    outputs = self.model.generate(**generation_config)
                    output_tokens.append(outputs[0][-1].item())
                    print(self.tokenizer.decode([output_tokens[-1]], skip_special_tokens=True), end='', flush=True)
                inferred_text = self.tokenizer.decode(output_tokens, skip_special_tokens=True)
            else:
                outputs = self.model.generate(**generation_config)
                inferred_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            split_text = inferred_text.split(".")
            if mode == "short" and len(split_text) > 1:
                inferred_text = split_text[0] + "."
            elif mode == "medium" and len(split_text) > 2:
                inferred_text = ".".join(split_text[:2]) + "."
            elif mode == "long" and len(split_text) > 3:
                inferred_text = ".".join(split_text[:3]) + "."

            return inferred_text.strip()
        except Exception as e:
            raise ValueError(f"An error occurred during text inferencing: {str(e)}")

    def chat_with_assistant(self, max_length=100, temperature=0.7, top_p=0.9, max_context_tokens=2048):
        context_history = "assistant: "
        stop_characters = ".!?"

        while True:
            user_input = input("You: ")
            context_history += f"user: {user_input}"

            tokens = self.tokenizer.encode(context_history, add_special_tokens=False)
            if len(tokens) > max_context_tokens:
                tokens = tokens[-max_context_tokens:]
            context = self.tokenizer.decode(tokens)

            try:
                inferred_text = self.infer_text(f"{context}assistant: ", max_length=max_length, temperature=temperature, top_p=top_p)
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

            assistant_responses = inferred_text.split("assistant: ")[-1]

            # Look for the first stop character to end the assistant's response
            assistant_response = ""
            for char in assistant_responses:
                assistant_response += char
                if char in stop_characters:
                    break

            if assistant_response.strip():  # Check if the assistant's response is not empty
                print(f"Assistant: {assistant_response}")
                context_history += f"assistant: {assistant_response}"
            else:
                print("Assistant: I didn't catch that, could you please repeat?")

            if user_input.lower() == "quit" or user_input.lower() == "exit":
                break


def select_path():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select the directory containing model and tokenizer files")
    return folder_selected

def display_menu():
    print(Fore.CYAN + "\nInfernoLM: The Language Model Inferencer\n")
    print("1. Infer Text")
    print("2. Switch Model")
    print("3. Toggle Real-time Token Output")
    print("4. Chat with Assistant")
    print("5. Exit")
    print(Style.RESET_ALL)

def main():
    print(Fore.GREEN + "Welcome to InfernoLM: The Language Model Inferencer!")
    model_path = select_path()
    if not model_path:
        print("No directory selected. Exiting.")
        return

    device_choice = input("\nSelect the device (cpu/gpu): ")
    if device_choice == "gpu":
        if torch.cuda.is_available():
            device_choice = "cuda"
            precision = input("Select the precision (float32 or float16): ")
        else:
            print("GPU not found. Defaulting to CPU.")
            device_choice = "cpu"
            precision = "float32"
    else:
        precision = "float32"

    inferencer = InfernoLM(device=device_choice, precision=precision, model_path=model_path)
    real_time_output = False
    while True:
        display_menu()
        choice = input("Enter your choice (1, 2, 3, 4, or 5): ")
        if choice == "1":
            prompt = input("\nEnter your prompt: ")
            mode = input("Select the mode (short, medium, long, full, custom): ")

            if mode == "custom":
                max_length = int(input("Define the maximum length (e.g., 100): "))
            else:
                max_length = 500

            temperature = float(input("Set the temperature (e.g., 0.7): "))
            print(Fore.YELLOW)
            inferred_text = inferencer.infer_text(prompt, mode, max_length, temperature, real_time=real_time_output)
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
            real_time_output = not real_time_output
            status = "ON" if real_time_output else "OFF"
            print(f"Real-time Token Output is now {status}")
        elif choice == "4":
            print("\nEntering Chatbot Mode. Type 'quit' or 'exit' to leave.")
            inferencer.chat_with_assistant(max_length=500, temperature=0.7, top_p=0.9)
        elif choice == "5":
            print(Fore.GREEN + "\nThank you for using InfernoLM. Farewell!")
            break
        else:
            print(Fore.RED + "\nInvalid selection. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
