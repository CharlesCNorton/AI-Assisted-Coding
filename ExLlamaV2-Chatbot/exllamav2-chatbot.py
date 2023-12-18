import os
import sys
import tkinter as tk
from tkinter import filedialog
import argparse
import torch
import time

def select_model_directory():
    root = tk.Tk()
    root.withdraw()
    model_dir = filedialog.askdirectory(title="Select the Model Directory")
    root.destroy()
    return model_dir

model_dir = select_model_directory()
if not model_dir:
    print("No model directory selected. Exiting.")
    sys.exit(1)

exllamav2_path = os.path.abspath("C:/Users/cnort/Documents/GitHub/exllamav2/exllamav2")
exllamav2_ext_path = os.path.abspath("C:/Users/cnort/Documents/GitHub/exllamav2/exllamav2/exllamav2_ext")

os.environ['PATH'] = exllamav2_ext_path + os.pathsep + os.environ['PATH']
sys.path.append(exllamav2_path)

try:
    from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache
    from exllamav2.generator import ExLlamaV2BaseGenerator, ExLlamaV2Sampler
    import model_init
except ImportError as e:
    print(f"Failed to import exllamav2 modules: {e}")
    sys.exit(1)

args = argparse.Namespace()
args.model_dir = model_dir
args.vocab_size = 32000
args.hidden_size = 4096
args.intermediate_size = 14336
args.num_hidden_layers = 32
args.num_attention_heads = 32
args.num_key_value_heads = 8
args.hidden_act = 'silu'
args.max_position_embeddings = 131072
args.initializer_range = 0.02
args.rms_norm_eps = 1e-05
args.use_cache = True
args.pad_token_id = None
args.bos_token_id = 1
args.eos_token_id = 2
args.tie_word_embeddings = False
args.rope_theta = 1000000.0
args.sliding_window = 4096
args.attention_dropout = 0.0
args.num_experts_per_tok = 2
args.num_local_experts = 8
args.output_router_logits = False
args.router_aux_loss_coef = 0.001
args.length = 1024
args.rope_scale = 1.0
args.rope_alpha = 1.0
args.no_flash_attn = False
args.low_mem = False
args.gpu_split = False

try:
    model, tokenizer = model_init.init(args)
except Exception as e:
    print(f"Error during model initialization: {e}")
    sys.exit(1)

cache = ExLlamaV2Cache(model)
generator = ExLlamaV2BaseGenerator(model, cache, tokenizer)

MAX_TOKENS = 32000

class Conversation:
    def __init__(self, tokenizer):
        self.history = []
        self.tokenizer = tokenizer

    def add_exchange(self, user_input, bot_response):
        self.history.append({"user": user_input, "bot": bot_response})
        self.trim_history()

    def get_context(self):
        context = ""
        for exchange in self.history:
            context += f'You: {exchange["user"]}\nBot: {exchange["bot"]}\n'
        return context

    def trim_history(self):
        while len(self.history) > 0:
            tokens = self.tokenizer.encode(self.get_context())
            if len(tokens) <= MAX_TOKENS:
                break
            self.history.pop(0)

def generate_text(prompt, generator, tokenizer, settings, max_new_tokens):
    time_begin = time.time()
    response = generator.generate_simple(prompt, settings, max_new_tokens)
    response = response[len(prompt):]
    time_end = time.time()
    time_total = time_end - time_begin
    tokens = tokenizer.encode(response)
    count = len(tokens)
    print(f"Response generated in {time_total:.2f} seconds, {count} tokens, {count / time_total:.2f} tokens/second, character len: {len(response)}")
    return response

def chat():
    conversation = Conversation(tokenizer)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break

        context = conversation.get_context() + f'You: {user_input}\n'
        try:
            with torch.inference_mode():
                settings = ExLlamaV2Sampler.Settings()
                settings.temperature = 0.9
                settings.top_k = 40
                settings.top_p = 0.9

                output = generate_text(context, generator, tokenizer, settings, 50)
                print("Bot:", output)

                conversation.add_exchange(user_input, output)
        except Exception as e:
            print(f"Error during response generation: {e}")

def main():
    print("Welcome to the ExLlamaV2 Chatbot!")
    try:
        chat()
    except KeyboardInterrupt:
        print("\nExiting chatbot. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
