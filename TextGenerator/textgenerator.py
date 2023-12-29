import os
import logging
import warnings
import torch
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore, Back, Style
from transformers import AutoTokenizer, AutoModelForCausalLM
import traceback
import pyttsx3
from abc import ABC, abstractmethod

init(autoreset=True)

class TTSStrategy(ABC):
    @abstractmethod
    def speak(self, text):
        pass

class Pyttsx3Strategy(TTSStrategy):
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print_colored("Error in Pyttsx3 TTS: " + str(e), color=Fore.RED)

def print_colored(text, color=Fore.WHITE, on_color='', attrs=[], end='\n'):
    print(f"{color}{on_color}{''.join(attrs)}{text}{Style.RESET_ALL}", end=end)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.basicConfig(level=logging.INFO)
logging.getLogger('tensorflow').setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

class InfernoLM:
    def __init__(self, device="cpu", precision="float32", model_path=None, verbose=False, tts_strategy=None):
        self.device = device
        self.precision = precision
        self.model_path = model_path
        self.verbose = verbose
        self.tts_strategy = tts_strategy
        self.tts_enabled = False if tts_strategy is None else True
        if model_path:
            self.tokenizer, self.model = self._load_model_and_tokenizer()

    def _load_model_and_tokenizer(self):
        print_colored("Loading model and tokenizer...", color=Fore.YELLOW)
        tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True)
        model.config.pad_token_id = model.config.eos_token_id
        tokenizer.pad_token = tokenizer.eos_token
        model.to(device=self.device, dtype=torch.float16 if self.precision == "float16" else torch.float32)
        return tokenizer, model

    def toggle_verbose_logging(self):
        self.verbose = not self.verbose
        logging_level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=logging_level)
        print_colored(f"Verbose logging {'enabled' if self.verbose else 'disabled'}.", color=Fore.BLUE)

    def load_model(self):
        model_path = select_path()
        if model_path:
            self.model_path = model_path
            self.choose_device()
            self.choose_precision()

            self.tokenizer, self.model = self._load_model_and_tokenizer()
            print_colored(f"Model loaded from {model_path}", color=Fore.CYAN)
        else:
            print_colored("No directory selected.", color=Fore.RED)

    def choose_device(self):
        device_choice = input("Choose device (GPU/CPU): ").strip().lower()
        if device_choice == "gpu" and torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"
        print_colored(f"Selected {self.device} device.", color=Fore.MAGENTA)

    def choose_precision(self):
        precision_choice = input("Choose precision (float32/float16): ").strip().lower()
        if precision_choice == "float16":
            self.precision = "float16"
        else:
            self.precision = "float32"
        print_colored(f"Selected {self.precision} precision.", color=Fore.GREEN)

    def toggle_tts(self):
        self.tts_enabled = not self.tts_enabled
        status = 'enabled' if self.tts_enabled else 'disabled'
        print_colored(f"TTS {status}.", color=Fore.BLUE)

    def chat_with_assistant(self):
        system_prompt = "You are a helpful, respectful, and honest assistant."
        context_history = f"<s>[INST] <<SYS>> {system_prompt} <</SYS>>\nAssistant: How may I help you?\n"

        print_colored("Assistant: How may I help you?", color=Fore.CYAN)

        while True:
            # Print "You: " with color only
            print_colored("You: ", color=Fore.LIGHTYELLOW_EX, end='')

            user_input = input()
            if user_input.lower() in ["quit", "exit"]:
                break

            context_history += f"[user_message: {user_input}]\n"

            inputs = self.tokenizer.encode_plus(
                context_history, return_tensors='pt', padding=True, truncation=True, max_length=4096
            )
            inputs = inputs.to(self.device)

            try:
                generation_length = 1000
                generation_config = {
                    'input_ids': inputs['input_ids'],
                    'max_length': len(inputs['input_ids'][0]) + generation_length,
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'top_k': 50,
                    'pad_token_id': self.tokenizer.eos_token_id,
                    'do_sample': True,
                    'early_stopping': True
                }

                outputs = self.model.generate(**generation_config)
                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                # Extracting assistant's response
                assistant_response = generated_text.split(f"[user_message: {user_input}]")[-1]
                assistant_response = assistant_response.split("<s>")[0].strip()

                # Check if the response already starts with "Assistant:"
                if not assistant_response.startswith("Assistant:"):
                    assistant_response = f"Assistant: {assistant_response}"

                print_colored(assistant_response, color=Fore.CYAN)

                context_history += f"<s>[INST] {assistant_response} </s><s>[INST]"

                if self.verbose:
                    logging.debug(f"Current context: {context_history}")

            except Exception as e:
                print_colored("An error occurred during generation.", color=Fore.RED)
                logging.error("An error occurred during generation:", exc_info=True)

    def extract_response(self, generated_text, user_input):
        split_text = generated_text.split(f"[user_message: {user_input}]")
        if len(split_text) > 1:
            return split_text[1].split("<s>")[0].strip()
        else:
            return "I'm sorry, I couldn't generate a proper response."

def select_path():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select the directory containing model and tokenizer files")
    return folder_selected

def display_menu():
    menu_text = "\nInfernoLM: The Language Model Inferencer\n\n" + \
                "1. Load Model\n" + \
                "2. Chat with Assistant\n" + \
                "3. Toggle Verbose Logging\n" + \
                "4. Exit\n" + \
                "5. Toggle Text-to-Speech\n"
    print_colored(menu_text, color=Fore.YELLOW, attrs=['bold'])

def main():
    print_colored("Welcome to InfernoLM: The Language Model Inferencer!", color=Fore.GREEN, attrs=['bold'])

    tts_strategy = Pyttsx3Strategy()

    inferencer = InfernoLM(tts_strategy=tts_strategy)

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            inferencer.load_model()
        elif choice == "2":
            if inferencer.model_path:
                print_colored("\nEntering Chatbot Mode. Type 'quit' or 'exit' to leave.", color=Fore.BLUE)
                inferencer.chat_with_assistant()
            else:
                print_colored("No model loaded. Please load a model first.", color=Fore.RED)
        elif choice == "3":
            inferencer.toggle_verbose_logging()
        elif choice == "4":
            print_colored("\nThank you for using InfernoLM. Farewell!", color=Fore.GREEN)
            break
        elif choice == "5":
            inferencer.toggle_tts()
        else:
            print_colored("\nInvalid selection. Please enter a number between 1 and 5.", color=Fore.RED)

if __name__ == "__main__":
    main()
