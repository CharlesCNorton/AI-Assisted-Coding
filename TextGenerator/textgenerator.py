import os
import warnings
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import traceback
import threading
import librosa
from llama_cpp import Llama
import sys

os.environ['NUMEXPR_MAX_THREADS'] = '32'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore")

class InfernoLM:
    def __init__(self, device="cpu", precision="float32", model_path=None, verbose=False, inference_engine="transformers"):
        self.device = device
        self.precision = precision
        self.model_path = model_path
        self.inference_engine = inference_engine
        if model_path:
            self.tokenizer, self.model = self._load_model_and_tokenizer()

    def _load_model_and_tokenizer(self):
        if self.inference_engine == "transformers":
            print("Loading model and tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
            model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True)
            model.config.pad_token_id = model.config.eos_token_id
            tokenizer.pad_token = tokenizer.eos_token
            model.to(device=self.device, dtype=torch.float16 if self.precision == "float16" else torch.float32)
            return tokenizer, model

        elif self.inference_engine == "llama.cpp":
            print("Loading LLaMA model...")
            model = Llama(model_path=self.model_path, n_ctx=4096)
            return None, model


    def chat_with_assistant(self):
        if self.inference_engine == "transformers":
            system_prompt = "You are a helpful, respectful, and honest assistant."
            context_history = f"<s>[INST] <<SYS>> {system_prompt} <</SYS>>\nAssistant: How can I help you?\n"
            self._print_assistant_message("How can I help you?")
            while True:
                self._print_user_prompt()
                user_input = input()
                if user_input.lower() in ["quit", "exit"]:
                    break
                context_history += f"[user_message: {user_input}]\n"
                inputs = self.tokenizer.encode_plus(context_history, return_tensors='pt', padding=True, truncation=True, max_length=4096)
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
                    assistant_response = self.extract_response(generated_text, user_input)
                    self._print_assistant_message(assistant_response)
                    context_history += f"<s>[INST] {assistant_response} </s><s>[INST]"
                except Exception as e:
                    self._print_assistant_message("An error occurred during generation.")


        if self.inference_engine == "llama.cpp":
            print("LLaMA chat mode activated. Type 'quit' or 'exit' to end the chat.")
            conversation_history = "Assistant: How can I help you?"
            self._print_assistant_message("How can I help you?")

            while True:
                self._print_user_prompt()
                user_input = input().strip()

                if user_input.lower() in ["quit", "exit"]:
                    print("Exiting chat mode.")
                    break

                conversation_history += f"\nUser: {user_input}\n"

                try:
                    output = self.model(
                        conversation_history + "Assistant: ",
                        max_tokens=1000,
                        stop=["\n"],
                        echo=True
                    )
                    assistant_response = output['choices'][0]['text'].strip()
                    self._print_assistant_message(assistant_response)

                    conversation_history += assistant_response

                except Exception as e:
                    print(f"An error occurred during generation: {e}")

    def extract_response(self, generated_text, user_input):
        split_text = generated_text.split(f"[user_message: {user_input}]")
        if len(split_text) > 1:
            return split_text[1].split("<s>")[0].strip()
        else:
            return "I'm sorry, I couldn't generate a proper response."

    def _print_assistant_message(self, message):
        print(f"\nAssistant: {message}\n")

    def _print_user_prompt(self):
        print("You: ", end='')
    def load_model(self, model_path):
        self.model_path = model_path
        self.choose_device()

        if self.inference_engine == "transformers":
            self.choose_precision()

        self.tokenizer, self.model = self._load_model_and_tokenizer()
        print(f"Model loaded from {model_path}")

    def choose_device(self):
        if self.inference_engine == "transformers":
            device_choice = input("Choose device (GPU/CPU): ").strip().lower()
            if device_choice == "gpu" and torch.cuda.is_available():
                self.device = "cuda"
            else:
                self.device = "cpu"
            print(f"Selected {self.device} device.")
        else:
            print("Device selection is only available for Transformers inference engine.")

    def choose_precision(self):
        precision_choice = input("Choose precision (float32/float16): ").strip().lower()
        if precision_choice == "float16":
            self.precision = "float16"
        else:
            self.precision = "float32"
        print(f"Selected {self.precision} precision.")

    def choose_inference_engine(self):
        engine_choice = input("Choose inference engine (Transformers/llama.cpp): ").strip().lower()
        if engine_choice in ["transformers", "llama.cpp"]:
            self.inference_engine = engine_choice
        else:
            print("Invalid choice. Defaulting to Transformers.")
            self.inference_engine = "transformers"
        print(f"Selected {self.inference_engine} as the inference engine.")

        if self.inference_engine == "transformers":
            self.choose_device()

    def set_gpu_layers(self):
        if self.inference_engine == "llama.cpp":
            try:
                n_layers = int(input("Enter the number of layers to offload to GPU (0 for CPU only): "))
                self.n_gpu_layers = max(0, n_layers)
                print(f"Set to offload {self.n_gpu_layers} layers to GPU.")
            except ValueError:
                print("Invalid input. No layers will be offloaded to GPU.")
                self.n_gpu_layers = 0
        else:
            print("GPU layer setting is only available for llama.cpp.")

    def display_menu():
        menu_text = "\nInfernoLM: The Language Model Inferencer\n\n" + \
                    "1. Chat with Assistant\n" + \
                    "2. Load Model\n" + \
                    "3. Exit\n"
        print(menu_text)

def main():
    print("Welcome to InfernoLM: The Language Model Inferencer!")
    inferencer = InfernoLM()

    while True:
        print("\nInfernoLM: The Language Model Inferencer\n")
        menu_options = [
            "1. Chat with Assistant",
            "2. Load Model",
            f"3. Toggle Inference Engine (Currently: {inferencer.inference_engine})"
        ]

        if inferencer.inference_engine == "llama.cpp":
            menu_options.append("4. Set GPU Layers")

        menu_options.append("5. Exit")

        for option in menu_options:
            print(option)

        choice = input("Enter your choice: ")

        if choice == "2":
            model_path = input("Enter the model path: ")
            inferencer.load_model(model_path)
        elif choice == "1":
            if inferencer.model_path:
                print("\nEntering Chatbot Mode. Type 'quit' or 'exit' to leave.")
                inferencer.chat_with_assistant()
            else:
                print("No model loaded. Please load a model first.")
        elif choice == "3":
            if inferencer.inference_engine == "transformers":
                inferencer.inference_engine = "llama.cpp"
            else:
                inferencer.inference_engine = "transformers"
            print(f"Inference engine switched to {inferencer.inference_engine}")
            if inferencer.inference_engine == "transformers":
                inferencer.choose_device()
        elif choice == "4" and inferencer.inference_engine == "llama.cpp":
            inferencer.set_gpu_layers()
        elif choice == "5":
            print("\nThank you for using InfernoLM. Farewell!")
            break

if __name__ == "__main__":
    main()
