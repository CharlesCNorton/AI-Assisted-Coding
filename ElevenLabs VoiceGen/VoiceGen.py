import requests
import os
import re

BASE_URL = "https://api.elevenlabs.io/v1"
API_KEY = "YOUR_API_KEY"  # Placeholder
DEFAULT_DIR = "./"  # Set current directory as the default directory

def sanitize_filename(filename):
    """Sanitize the filename to remove unwanted characters."""
    sanitized_name = re.sub(r'[^a-zA-Z0-9_\-]', '', filename)
    return sanitized_name or "output.mp3"

def initialize_api_key():
    """Prompt the user to enter their API key at startup if it's not set."""
    global API_KEY
    if API_KEY == "YOUR_API_KEY":
        API_KEY = input("Please enter your ElevenLabs API key: ")

def fetch_api_data(endpoint, headers):
    """General function to fetch data from API."""
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else", err)

def get_voices():
    """Fetch available voices from the ElevenLabs API."""
    headers = {"xi-api-key": API_KEY}
    return fetch_api_data("voices", headers)

def display_voices(voices):
    """Display the available voices."""
    for index, voice in enumerate(voices, 1):
        print(f"{index}. {voice['name']} ({voice['voice_id']})")

def select_voice(voices):
    """Prompt the user to select a voice and return the selected voice."""
    while True:
        try:
            selected = int(input("\nSelect a voice number or 0 to return to main menu: "))
            if 0 < selected <= len(voices):
                return voices[selected - 1]
            elif selected == 0:
                return None
            else:
                print("\nInvalid voice number.")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

def handle_text_to_speech_response(response, filename):
    """Handle the response for text to speech conversion."""
    try:
        if response.status_code == 200:
            full_path = os.path.join(DEFAULT_DIR, filename)
            with open(full_path, 'wb') as audio_file:
                audio_file.write(response.content)
            print(f"Audio saved as {full_path}")
        else:
            print(f"Error: {response.json().get('message', response.text)}")
    except PermissionError:
        print("Permission denied. Try saving the file in a different directory or with a different filename.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def text_to_speech(text, voice_id):
    """Convert given text to speech using a specified voice."""
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
    try:
        response = requests.post(
            f"{BASE_URL}/text-to-speech/{voice_id}",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        handle_text_to_speech_response(response)
    except requests.exceptions.RequestException as e:
        print(f"Error in text-to-speech request: {e}")

def main():
    """Main driver function."""
    global DEFAULT_DIR

    initialize_api_key()

    print("Welcome to ElevenLabs VoiceGen!")
    print("=" * 30)
    selected_voice = None

    while True:
        print("\n=== Menu ===")
        print("1. List Available Voices")
        print("2. Convert Text to Speech")
        print("3. Set Default Output Directory")
        print("4. Exit")
        choice = input("\nYour choice: ")

        if choice == "1":
            voices_data = get_voices()
            if voices_data:
                voices = voices_data['voices']
                display_voices(voices)
                selected_voice = select_voice(voices)
                if selected_voice:
                    print(f"\nYou've selected: {selected_voice['name']} ({selected_voice['voice_id']})")
        elif choice == "2":
            text = input("\nEnter the text you want to convert to speech: ")
            if not text.strip():
                print("\nPlease provide some text.")
                continue

            voice_id = input("Enter the voice ID (or leave empty to use a previously selected voice if any): ") or (selected_voice and selected_voice['voice_id'])

            if not voice_id:
                print("\nPlease provide a voice ID or select a voice first.")
                continue
            filename = input("Enter a filename for the audio output (without extension, e.g., myaudio): ")
            filename = sanitize_filename(filename) + ".mp3"
            text_to_speech(text, voice_id, filename)
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