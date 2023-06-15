"""
GPT-3.5 Turbo Console Chat Application
Created with GPT-4
Date: June 15, 2023
"""

# Import necessary modules
import openai
import time
import threading
from colorama import Fore, Style, init
import itertools
import os

# Initialize colorama
init(autoreset=True)

# Set OpenAI API key and organization ID
openai.api_key = "INSERT_YOUR_API_KEY_HERE"
openai.organization = "INSERT_YOUR_ORG_HERE"

# Define conversation directory and the threshold for re-inserting system message
CONVO_DIR = "POINT_TO_PREFERRED_DIRECTORY"
TIME_BETWEEN_SYSTEM_MESSAGES = 5000  # In characters

# Function to display a loading animation during API calls
def show_loading_animation(event):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while not event.is_set():
        print(next(spinner), end='\r')
        time.sleep(0.1)

# Function to call the OpenAI API
def call_openai_api(messages, temperature):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            temperature=temperature,
            max_tokens=200
        )
        if response.choices:
            return response.choices[0].message['content']
    except openai.api_errors.RateLimitError as e:
        print(Fore.RED + f"API rate limit exceeded: {e}")
    except openai.api_errors.AuthenticationError as e:
        print(Fore.RED + f"Authentication error: {e}")
    except openai.api_errors.APIError as e:
        print(Fore.RED + f"General API error: {e}")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
    return ""

# Function to load a saved conversation from a file
def load_conversation(filename):
    try:
        with open(f"{CONVO_DIR}/{filename}.txt", 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(Fore.RED + f"No such file named '{filename}'")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

# Function to save the current conversation to a file
def save_conversation(conversation_history, filename):
    try:
        os.makedirs(CONVO_DIR, exist_ok=True)
        with open(f"{CONVO_DIR}/{filename}.txt", 'w') as file:
            for msg in conversation_history:
                file.write(msg['role'] + ": " + msg['content'] + '\n')
        print(Fore.GREEN + f"Conversation saved under name '{filename}'")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

# Main function that runs the chatbot
def main():
    # Welcome message
    print(Fore.GREEN + "\n=== Welcome to GPT-3.5 Chat ===" + Style.RESET_ALL)
    print("1. Set Assistant's Personality")
    print("2. Set Response Randomness (Temperature)")
    print("3. Start Chatting")
    print("4. Load Previous Conversation")
    print("5. Help")

    # Default system message and temperature
    system_message = "You are an extremely helpful and innovative science bot."
    temperature = 0.8

    # Menu loop
    while True:
        choice = input("Choose an option: ")

        if choice == '1':
            system_message = input("Enter the system message for the assistant: ")
        elif choice == '2':
            temperature = float(input("Enter a temperature between 0 and 1: "))
        elif choice == '3':
            break
        elif choice == '4':
            filename = input("Enter filename to load: ")
            loaded_data = load_conversation(filename)
            if loaded_data:
                print(loaded_data)
            continue
        elif choice == '5':
            print("Assistant's Personality (System Message): " + system_message)
            print("Response Randomness (Temperature): " + str(temperature))
            continue
        else:
            print(Fore.RED + "Invalid choice. Please choose 1, 2, 3, 4 or 5.")

    # Initialize conversation history with system message and character count
    conversation_history = [{"role": "system", "content": system_message}]
    conversation_character_count = len(system_message)

    # Conversation loop
    while True:
        user_message = input(Fore.GREEN + "\nUser: " + Style.RESET_ALL)

        if user_message.lower() == 'save':
            filename = input("Enter filename to save: ")
            save_conversation(conversation_history, filename)
            continue
        elif user_message.lower() == 'menu':
            main()
            return
        elif user_message.lower() == 'help':
            print("Current System Message: " + system_message)
            print("Current Temperature: " + str(temperature))
            continue

        # Add user message to history and update character count
        conversation_history.append({"role": "user", "content": user_message})
        conversation_character_count += len(user_message)

        # Display loading animation while making API call
        finished = threading.Event()
        loading_thread = threading.Thread(target=show_loading_animation, args=(finished,))
        loading_thread.start()

        # Re-insert system message after a certain amount of characters
        if conversation_character_count >= TIME_BETWEEN_SYSTEM_MESSAGES:
            conversation_history.append({"role": "system", "content": system_message})
            conversation_character_count = 0

        # Call OpenAI API and get response
        response_message = call_openai_api(conversation_history, temperature)
        finished.set()

        # Print bot's response and add to history
        print(Fore.CYAN + f"GPT-3.5: {response_message}")
        conversation_history.append({"role": "assistant", "content": response_message})
        conversation_character_count += len(response_message)

        # Truncate history if it gets too long
        if len(''.join(msg['content'] for msg in conversation_history)) > 37000:
            conversation_history = conversation_history[-10:]

# Run the main function
if __name__ == "__main__":
    main()
