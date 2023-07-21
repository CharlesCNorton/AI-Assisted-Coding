from transformers import AutoTokenizer, AutoModelForCausalLM, GPT2LMHeadModel, GPT2Tokenizer
import torch
import gc
class TextGenerator:
    def __init__(self, model_name="gpt2", device="cuda:0", precision="float32", use_sequential_execution=False):
        self.model_name = model_name
        self.device = device
        self.precision = precision
        self.use_sequential_execution = use_sequential_execution
        torch.cuda.empty_cache()
        gc.collect()
        self.tokenizer, self.model = self._load_model_and_tokenizer()
    def _load_model_and_tokenizer(self):
        try:
            if "Llama-2-13b-hf" in self.model_name:
                tokenizer = AutoTokenizer.from_pretrained('SET_PATH', local_files_only=True)
                tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                model = AutoModelForCausalLM.from_pretrained('SET_PATH', local_files_only=True).to(device=self.device, dtype=torch.float16 if self.precision=="float16" else torch.float32)
            elif "Llama-2-7b-hf" in self.model_name:
                tokenizer = AutoTokenizer.from_pretrained('SET_PATH', local_files_only=True)
                tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                model = AutoModelForCausalLM.from_pretrained('SET_PATH', local_files_only=True).to(device=self.device, dtype=torch.float16 if self.precision=="float16" else torch.float32)
            elif "gpt2-xl" in self.model_name:
                tokenizer = GPT2Tokenizer.from_pretrained('SET_PATH', local_files_only=True)
                tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                tokenizer.padding_side = 'left'
                model = GPT2LMHeadModel.from_pretrained('SET_PATH', local_files_only=True).to(device=self.device, dtype=torch.float16 if self.precision=="float16" else torch.float32)
            return tokenizer, model
        except Exception as e:
            raise ValueError(f"An error occurred while loading the model: {str(e)}")
    def generate_text(self, prompt, max_length=100, temperature=0.7):
        try:
            if "Llama-2-13b-hf" in self.model_name or "Llama-2-7b-hf" in self.model_name:
                inputs = self.tokenizer(prompt, return_tensors='pt', padding=True, truncation=True, max_length=max_length).to(self.device)
                attention_mask = inputs['attention_mask'].type(torch.float16 if self.precision=="float16" else torch.float32)
                outputs = self.model.generate(input_ids=inputs['input_ids'], max_length=max_length, temperature=temperature, attention_mask=attention_mask)
                generated_text = self.tokenizer.decode(outputs[0])
            else:
                inputs = self.tokenizer(prompt, return_tensors='pt', padding=True, truncation=True, max_length=max_length).to(self.device)
                attention_mask = inputs['attention_mask'].type(torch.float16 if self.precision=="float16" else torch.float32)
                outputs = self.model.generate(input_ids=inputs['input_ids'], max_length=max_length, temperature=temperature, attention_mask=attention_mask)
                generated_text = self.tokenizer.decode(outputs[0])
            return generated_text
        except Exception as e:
            raise ValueError(f"An error occurred during text generation: {str(e)}")
def main():
    print("Welcome to the Text Generator!")
    text_generator = None
    while True:
        print("\nPlease choose an option:")
        print("1. Generate text")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ")
        if choice == "1":
            model_names = ["gpt2-xl", "meta-llama/Llama-2-13b-hf", "meta-llama/Llama-2-7b-hf"]
            try:
                if text_generator is None:
                    device_choice = input("\nEnter the device to use for inferencing (cpu/cuda:0): ")
                    print("\nSelect a model:")
                    print("1. gpt2-xl")
                    print("2. Llama-2-13b-hf")
                    print("3. Llama-2-7b-hf")
                    model_choice = input("Enter a number (1-3): ")
                    model_name = model_names[int(model_choice) - 1]
                    sequential_execution_choice = input("Do you want to use sequential execution? (yes/no): ")
                    use_sequential_execution = True if sequential_execution_choice.lower() == "yes" else False
                    if device_choice == "cuda:0":
                        precision = input("Enter the precision (float32 or float16): ")
                    else:
                        precision = "float32"
                    text_generator = TextGenerator(model_name, device=device_choice, precision=precision, use_sequential_execution=use_sequential_execution)
                prompt = input("\nEnter a prompt: ")
                max_length = int(input("\nEnter the maximum length of the generated text (e.g., 100): "))
                temperature = float(input("Enter the temperature for the generation process (e.g., 0.7): "))
                generated_text = text_generator.generate_text(prompt, max_length, temperature)
                print("\nGenerated Text:")
                print(generated_text)
                change_model = input("\nDo you want to change the model? (yes/no): ")
                if change_model.lower() == "yes":
                    del text_generator
                    torch.cuda.empty_cache()
                    text_generator = None
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
        elif choice == "2":
            print("\nThank you for using the Text Generator. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1 or 2.")
if __name__ == "__main__":
    main()
