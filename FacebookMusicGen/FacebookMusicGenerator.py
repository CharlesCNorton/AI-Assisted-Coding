import re
import scipy.io.wavfile
import traceback
import torchaudio
from colorama import init, Fore
from datetime import datetime
from pathlib import Path
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import torch
import tkinter as tk
from tkinter import filedialog

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
    """Handles the music generation process using an existing melody."""
    try:
        root = tk.Tk()
        root.withdraw()
        melody_path = filedialog.askopenfilename(title="Select a melody file", filetypes=[("Audio Files", "*.mp3 *.wav")])
        if not melody_path:
            colored_print(Fore.RED, "No melody file selected. Returning to main menu.")
            return

        descriptions = []
        while True:
            desc = input("Enter description (or hit Enter to skip and finish): ").strip()
            if not desc:
                break
            descriptions.append(desc)

        model = MusicGen.get_pretrained('facebook/musicgen-melody')
        model.set_generation_params(duration=8)
        melody, sr = torchaudio.load(melody_path)

        wav = model.generate_with_chroma(descriptions, melody[None].expand(len(descriptions), -1, -1), sr)
        
        for idx, one_wav in enumerate(wav):
            output_file_name = f"melody_based_{idx}.wav"
            output_path = OUTPUT_PATH / output_file_name
            audio_write(str(output_path), one_wav.cpu(), model.sample_rate, strategy="loudness")
            colored_print(Fore.GREEN, f"Generated melody-based music saved as {output_file_name}")

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

        choice = input("Enter your choice: ").strip()
        if choice in MODEL_MAP:
            generate_music(MODEL_MAP[choice])
        elif choice.lower() == 'q':
            colored_print(Fore.GREEN, "Thank you for using MusicGen. Goodbye!")
            break
        elif choice.lower() == 't':
            toggle_device()
        elif choice.lower() == 'm':
            generate_music_with_melody()
        else:
            colored_print(Fore.RED, "Invalid input. Please enter a valid option.")

if __name__ == "__main__":
    main()