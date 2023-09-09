from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile
from pathlib import Path  # Imported pathlib for more intuitive file operations
import traceback
import re
from datetime import datetime
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Constants
MODEL_MAP = {
    "1": "facebook/musicgen-small",
    "2": "facebook/musicgen-medium",
    "3": "facebook/musicgen-large",
}
OUTPUT_PATH = Path("ENTER_YOUR_DESIRED_PATH")  # Changed to use pathlib.Path

# Function to validate filename
def validate_filename(filename: str) -> str:
    if not re.match("^[\w\-\_]*$", filename) or not filename:
        return datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
    return f"{filename}.wav"

# Function to load model
def load_model(model_name: str):
    return MusicgenForConditionalGeneration.from_pretrained(model_name)

# Function to generate audio from text
def generate_audio(model, text: str):
    processor = AutoProcessor.from_pretrained(model.config.name_or_path)
    inputs = processor(text=[text], padding=True, return_tensors="pt")
    return model.generate(**inputs, max_new_tokens=256)[0, 0].numpy()

def generate_music(model_name: str):
    try:
        # Load model
        model = load_model(model_name)

        # Get and validate text input
        text = input("Enter the text you want to convert to music (Cannot be empty): ").strip()
        if not text or len(text) > 1000:
            print(f"{Fore.RED}Text input was empty or too long. Please try again.")
            return

        # Generate audio
        audio_array = generate_audio(model, text)

        # Validate and generate filename
        filename = validate_filename(input("Enter a name for the output file: ").strip())

        # Write audio to file
        sampling_rate = model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(OUTPUT_PATH / filename, rate=sampling_rate, data=audio_array)

        print(f"Music has been successfully saved to {filename}")

    except OSError:
        print(f"{Fore.RED}An error occurred while trying to load the model or write the file.")
        print(traceback.format_exc())
    except ValueError:
        print(f"{Fore.RED}An error occurred during text processing or music generation.")
        print(traceback.format_exc())
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}")
        print(traceback.format_exc())

def main():
    while True:
        print(f"{Fore.BLUE}# Welcome to the Facebook Music Generator!")
        print(f"{Fore.GREEN}# Please select a model:")
        for k, v in MODEL_MAP.items():
            print(f"{Fore.YELLOW}# {k}: {v.split('/')[-1]}")
        print(f"{Fore.RED}# q: Quit")

        user_input = input("Enter your choice: ").strip()
        if user_input.isdigit() and user_input in MODEL_MAP:
            generate_music(MODEL_MAP[user_input])
        elif user_input.lower() == 'q':
            print("Thank you for using MusicGen. Goodbye!")
            break
        else:
            print(f"{Fore.RED}Invalid input. Please enter a valid option.")

if __name__ == "__main__":
    main()
