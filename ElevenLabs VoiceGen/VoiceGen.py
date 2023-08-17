import requests
import os

BASE_URL = "https://api.elevenlabs.io/v1"
API_KEY = "YOUR_API_KEY"  # Remember to add your API key here before executing
DEFAULT_DIR = "./"  # Set current directory as the default directory

def get_voices():
    headers = {
        "xi-api-key": API_KEY
    }
    response = requests.get(f"{BASE_URL}/voices", headers=headers)
    if response.status_code == 200:
        return response.json()["voices"]
    else:
        raise Exception(f"Error fetching voices: {response.status_code} - {response.text}")

def display_voices():
    voices = get_voices()
    for index, voice in enumerate(voices, 1):
        print(f"{index}. {voice['name']} ({voice['voice_id']})")
    return voices

def text_to_speech(text, voice_id):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.95,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }
    response = requests.post(
        f"{BASE_URL}/text-to-speech/{voice_id}",
        headers=headers,
        json=data
    )
    handle_response(response)

def handle_response(response):
    try:
        if response.status_code == 200:
            filename = input("Enter a filename for the audio output (e.g., myaudio.mp3): ")
            if not filename.strip():
                filename = "output.mp3"
            full_path = os.path.join(DEFAULT_DIR, filename)
            with open(full_path, 'wb') as audio_file:
                audio_file.write(response.content)
            print(f"Audio saved as {full_path}")
        else:
            error_details = response.json().get('message', response.text)
            print(f"Error: {error_details}")
    except PermissionError:
        print("Permission denied. Try saving the file in a different directory or with a different filename.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    global DEFAULT_DIR

    print("Welcome to ElevenLabs VoiceGen!")
    print("="*30)

    while True:
        print("\n=== Menu ===")
        print("1. List Available Voices")
        print("2. Convert Text to Speech")
        print("3. Set Default Output Directory")
        print("4. Exit")

        choice = input("\nYour choice: ")

        if choice == "1":
            voices = display_voices()
            selected = int(input("\nSelect a voice number or 0 to return to main menu: "))
            if 0 < selected <= len(voices):
                selected_voice = voices[selected-1]
                print(f"\nYou've selected: {selected_voice['name']} ({selected_voice['voice_id']})")
            elif selected != 0:
                print("\nInvalid voice number.")
        elif choice == "2":
            text = input("\nEnter the text you want to convert to speech: ")
            voice_id = input("Enter the voice ID (or leave empty to use a previously selected voice if any): ")
            if not voice_id and 'selected_voice' in locals():
                voice_id = selected_voice['voice_id']
            if not voice_id:
                print("\nPlease provide a voice ID or select a voice first.")
                continue
            text_to_speech(text, voice_id)
        elif choice == "3":
            dir_path = input("\nEnter the path for the default output directory (e.g., ./outputs/): ")
            if os.path.isdir(dir_path):
                DEFAULT_DIR = dir_path
                print(f"\nDefault directory set to: {DEFAULT_DIR}")
            else:
                print("\nThe provided path is not a valid directory. Please try again.")
        elif choice == "4":
            print("\nThank you for using ElevenLabs VoiceGen! Goodbye!")
            break
        else:
            print("\nInvalid choice! Please select 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()
