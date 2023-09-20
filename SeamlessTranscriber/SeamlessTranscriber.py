import sys
import os
import torch
import sounddevice as sd
import numpy as np
import torchaudio

sys.path.append('ENTER_PATH_HERE')

from seamless_communication.models.inference import Translator

def record_from_microphone(duration=10):
    """Record audio from the microphone and return the NumPy array."""
    samplerate = 16000
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    return audio.squeeze()

def transcribe_audio(model, audio_path=None):
    """Transcribe audio using the ASR model."""
    if not audio_path:
        audio = record_from_microphone()
        audio_path = 'temp_recording.wav'
        torchaudio.save(audio_path, torch.tensor(audio).unsqueeze(0), 16000)

    transcribed_text, _, _ = model.predict(audio_path, "asr", "en")
    return transcribed_text

def main():
    print("Initializing the SeamlessM4T model...")

    # Initialize the Translator object
    model_checkpoint = "ENTER_PATH_HERE"
    vocoder_checkpoint = "ENTER_PATH_HERE"
    translator = Translator(model_checkpoint, vocoder_name_or_card=vocoder_checkpoint, device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))

    print("\nSeamlessM4T model initialized!")

    while True:
        print("\nChoose an option:")
        print("1. Transcribe from a pre-recorded audio file.")
        print("2. Transcribe directly from the microphone.")
        print("3. Exit.")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            audio_path = input("Enter the path to the audio file: ")
            if os.path.exists(audio_path):
                print("\nTranscribing...")
                text = transcribe_audio(translator, audio_path)
                print("\nTranscribed Text:\n", text)
            else:
                print("\nFile not found. Please check the path and try again.")
        elif choice == '2':
            print("\nRecording audio from the microphone... (Duration: 10 seconds)")
            text = transcribe_audio(translator)
            print("\nTranscribed Text:\n", text)
        elif choice == '3':
            break
        else:
            print("\nInvalid choice. Please select a valid option.")

    print("\nThank you for using SeamlessM4T!")

if __name__ == "__main__":
    main()
