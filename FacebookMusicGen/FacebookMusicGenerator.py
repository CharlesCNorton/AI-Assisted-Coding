from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile
import os
import traceback
from datetime import datetime

from colorama import init, Fore, Back, Style
init(autoreset=True)

MODEL_MAP = {
    "1": "facebook/musicgen-small",
    "2": "facebook/musicgen-medium",
    "3": "facebook/musicgen-large",
}

def generate_music(model_name):
    try:
        model = MusicgenForConditionalGeneration.from_pretrained(model_name)

        text = input("Enter the text you want to convert to music (Cannot be empty): ")

        if not text.strip() or len(text) > 1000:
            print(Fore.RED + "Text input was empty or too long. Please try again with valid text (up to 1000 characters).")
            return

        processor = AutoProcessor.from_pretrained(model_name)
        inputs = processor(text=[text], padding=True, return_tensors="pt")

        audio_values = model.generate(**inputs, max_new_tokens=256)

        audio_array = audio_values[0, 0].numpy()

        filename = input("Enter a name for the output file (Cannot be empty for default name): ").strip()
        import re
        if not re.match("^[\w\-\_]*$", filename):
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        elif not filename:
            filename += ".wav"
            print("Invalid filename. Filename was empty, so a default filename has been used. For custom filenames, please use only alphanumeric characters, underscores, and hyphens.")
            return

        sampling_rate = model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(os.path.join("ENTER_YOUR_DESIRED_PATH", filename), rate=sampling_rate, data=audio_array)

        print(f"Music has been successfully saved to {filename}")

    except OSError as e:
        print("An error occurred while trying to load the model or write the file. Please check your internet connection and file system, and try again.")
        print(traceback.format_exc())
    except ValueError as e:
        print("An error occurred while trying to process the text input or generate the music. Please check your text input, and try again.")
        print(traceback.format_exc())
    except Exception as e:
        print("An unexpected error occurred: " + str(e))
        print(traceback.format_exc())

def main():
    while True:
        print(Fore.BLUE + "# Welcome to the Facebook Music Generator!")
        print(Fore.GREEN + "# Please select a model:")
        print(Fore.YELLOW + "# 1: Small Model")
        print(Fore.YELLOW + "# 2: Medium Model")
        print(Fore.YELLOW + "# 3: Large Model")
        print(Fore.RED + "# q: Quit")
        user_input = input("Enter your choice (1-4): ").strip()

        if user_input.isdigit() and user_input in MODEL_MAP:
            generate_music(MODEL_MAP[user_input])
        elif user_input.lower() == 'q':
            print("Thank you for using MusicGen. Goodbye!")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 3 or 'q' without any other characters.")

if __name__ == "__main__":
    main()
