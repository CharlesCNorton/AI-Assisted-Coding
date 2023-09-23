import re
import scipy.io.wavfile
import torchaudio
import traceback
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore
from datetime import datetime
from pathlib import Path
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import torch

init(autoreset=True)

MODEL_MAP = {
    "1": "facebook/musicgen-small",
    "2": "facebook/musicgen-medium",
    "3": "facebook/musicgen-large",
}
OUTPUT_PATH = Path("ENTER_PATH_HERE")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

def generate_music_with_melody():
    """Generate music based on melody and descriptions."""
    model = MusicGen.get_pretrained('facebook/musicgen-melody')
    model.set_generation_params(duration=30)

    root = tk.Tk()
    root.withdraw()
    melody_file = filedialog.askopenfilename(title="Select melody file")
    melody, sr = torchaudio.load(melody_file)

    descriptions = []
    while True:
        description = input("Enter description (or hit Enter to skip and finish): ")
        if not description:
            break
        descriptions.append(description)

    if not descriptions:
        descriptions = [""]

    wav = model.generate_with_chroma(descriptions, melody[None].expand(len(descriptions), -1, -1), sr)

    for idx, one_wav in enumerate(wav):
        output_file_name = OUTPUT_PATH / f"melody_based_{idx}.wav"
        audio_write(str(output_file_name), one_wav.cpu(), model.sample_rate, strategy="loudness")
        colored_print(Fore.GREEN, f"Generated melody-based music saved as {output_file_name.name}")

def generate_music(model_name: str):
    """Handles the entire music generation process."""
    try:
        model = load_model(model_name)
        batch_size = int(input("Enter batch size: ").strip())
        texts = [input(f"Enter text {i + 1} of {batch_size} (Can be empty): ").strip() for i in range(batch_size)]

        for text in texts:
            audio_array = generate_audio(model, text)

            if not OUTPUT_PATH.exists():
                OUTPUT_PATH.mkdir(parents=True)

            sampling_rate = model.config.audio_encoder.sampling_rate
            output_file = validate_filename(text)
            scipy.io.wavfile.write(OUTPUT_PATH / output_file, rate=sampling_rate, data=audio_array)
            colored_print(Fore.GREEN, f"Music for prompt '{text}' has been successfully saved to {output_file}")

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
        colored_print(Fore.MAGENTA, "# m: Generate Music with Melody")
        colored_print(Fore.CYAN, "# t: Toggle CPU/GPU")
        colored_print(Fore.RED, "# q: Quit")
        choice = input("Enter your choice: ").strip().lower()

        if choice == "q":
            break
        elif choice == "t":
            toggle_device()
        elif choice == "m":
            generate_music_with_melody()
        elif choice in MODEL_MAP:
            generate_music(MODEL_MAP[choice])
        else:
            colored_print(Fore.RED, "Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
