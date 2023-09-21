import re
import scipy.io.wavfile
import traceback
from colorama import init, Fore
from datetime import datetime
from pathlib import Path
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import torch

# Initialize colorama
init(autoreset=True)

# Constants
MODEL_MAP = {
    "1": "facebook/musicgen-small",
    "2": "facebook/musicgen-medium",
    "3": "facebook/musicgen-large",
}
OUTPUT_PATH = Path("ENTER_YOUR_DESIRED_PATH")

# Default device based on system configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Dictionary to store already loaded models.
loaded_models = {}

def colored_print(color: str, msg: str):
    """Prints colored messages."""
    print(f"{color}{msg}")

def validate_filename(filename: str) -> str:
    """Validates and returns a suitable filename."""
    if not re.match("^[\w\-\_]*$", filename) or not filename:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = OUTPUT_PATH / f"{filename}.wav"
    count = 1
    while full_filename.exists():
        full_filename = OUTPUT_PATH / f"{filename}_{count}.wav"
        count += 1
    return full_filename.name

def load_model(model_name: str):
    """Loads a pretrained model from HuggingFace hub."""
    global loaded_models
    # Check if the model is already loaded
    if model_name not in loaded_models:
        model = MusicgenForConditionalGeneration.from_pretrained(model_name)
        loaded_models[model_name] = model.to(device)
    return loaded_models[model_name]

def generate_audio(model, text: str):
    """Generates audio array from a given text using the provided model."""
    processor = AutoProcessor.from_pretrained(model.config.name_or_path)
    inputs = processor(text=[text], padding=True, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    return model.generate(**inputs, max_new_tokens=1408)[0, 0].cpu().numpy()

def toggle_device():
    """Toggle between CPU and CUDA GPU."""
    global device
    if device.type == "cuda":
        device = torch.device("cpu")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        colored_print(Fore.RED, "CUDA not available on this system. Staying on CPU.")
    colored_print(Fore.GREEN, f"Switched to {device.type.upper()}.")

def generate_music(model_name: str):
    """Handles the entire music generation process."""
    try:
        model = load_model(model_name)
        text = input("Enter the text you want to convert to music (Cannot be empty): ").strip()
        if not text or len(text) > 1000:
            colored_print(Fore.RED, "Text input was empty or too long. Please try again.")
            return

        audio_array = generate_audio(model, text)
        filename = validate_filename(input("Enter a name for the output file: ").strip())

        if not OUTPUT_PATH.exists():
            OUTPUT_PATH.mkdir(parents=True)

        sampling_rate = model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(OUTPUT_PATH / filename, rate=sampling_rate, data=audio_array)
        colored_print(Fore.GREEN, f"Music has been successfully saved to {filename}")

    except (OSError, ValueError) as e:
        colored_print(Fore.RED, f"An error occurred: {e}")
        print(traceback.format_exc())
    except Exception as e:
        colored_print(Fore.RED, f"An unexpected error occurred: {e}")
        print(traceback.format_exc())

def main():
    """Main driver function."""
    while True:
        colored_print(Fore.BLUE, "# Welcome to the Facebook Music Generator!")
        colored_print(Fore.GREEN, "# Please select a model:")
        for k, v in MODEL_MAP.items():
            colored_print(Fore.YELLOW, f"# {k}: {v.split('/')[-1]}")
        colored_print(Fore.CYAN, "# t: Toggle CPU/GPU")
        colored_print(Fore.RED, "# q: Quit")

        choice = input("Enter your choice: ").strip()
        if choice in MODEL_MAP:
            generate_music(MODEL_MAP[choice])
        elif choice.lower() == 'q':
            colored_print(Fore.GREEN, "Thank you for using MusicGen. Goodbye!")
            break
        elif choice.lower() == 't':
            toggle_device()
        else:
            colored_print(Fore.RED, "Invalid input. Please enter a valid option.")

if __name__ == "__main__":
    main()
