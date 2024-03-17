import os
from datetime import datetime
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from colorama import Fore, init
import pygame
import time

init(autoreset=True)
pygame.mixer.init()

def generate_bark_audio(text_prompt):
    """
    Generates audio from the provided text prompt using Bark, saves it to a WAV file with a unique timestamped name, and plays the audio.

    Parameters:
    - text_prompt (str): Text from which to generate audio.
    """
    try:
        audio_array = generate_audio(text_prompt)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"bark_output_{timestamp}.wav"

        write_wav(output_filename, SAMPLE_RATE, audio_array)
        print(Fore.GREEN + f"Audio successfully saved to {output_filename}")

        play_audio(output_filename)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

def play_audio(filename):
    """
    Plays the specified audio file using pygame.

    Parameters:
    - filename (str): The path to the audio file to play.
    """
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
        print(Fore.YELLOW + "Audio playback finished.")
    except Exception as e:
        print(Fore.RED + f"Error playing audio: {e}")

def main_menu():
    print(Fore.CYAN + "\nWelcome to Bark Audio Generator!")
    print(Fore.YELLOW + "1. Generate audio from text")
    print(Fore.YELLOW + "2. Exit")

def main():
    preload_models()
    while True:
        main_menu()
        choice = input(Fore.CYAN + "Choose an option: ").strip()

        if choice == "1":
            text_prompt = input(Fore.CYAN + "\nEnter your text prompt for audio generation: ").strip()
            generate_bark_audio(text_prompt)
        elif choice == "2":
            print(Fore.GREEN + "Exiting the program. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 1 to generate audio or 2 to exit.")

if __name__ == "__main__":
    main()
