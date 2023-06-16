#GPT-3.5 Turbo Console Chat Application
#Created with GPT-4
#Date: June 15, 2023
import openai
import time
import threading
import itertools
import os
import json
from colorama import Fore, Style, init
from rich import print
from rich.markdown import Markdown
init(autoreset=True)

openai.api_key = "USE_YOUR_OPENAI_API_KEY"
openai.organization = "USE_USE_OPENAI_ORG"
TIME_BETWEEN_SYSTEM_MESSAGES = 3000

def call_openai_api(messages, temperature):
    try:
        response = openai.ChatCompletion.create(
            model="USE_WHATEVER_MODEL",
            messages=messages,
            temperature=temperature,
            max_tokens=15000
        )
        if response.choices:
            return response.choices[0].message['content']
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
        return ""

def show_loading_animation(event):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while not event.is_set():
        print(next(spinner), end='\r')
        time.sleep(0.1)

def save_conversation(conversation, filename):
    path = f"ENTER_DIRECTORY\\{filename}.txt"
    try:
        with open(path, 'w') as file:
            json.dump(conversation, file)
        print(Fore.BLUE + f"Conversation saved to {path}")
    except Exception as e:
        print(Fore.RED + f"An error occurred while saving the conversation: {str(e)}")

def load_conversation(filename):
    path = f"ENTER_DIRECTORY\\{filename}.txt"
    try:
        if os.path.exists(path):
            with open(path, 'r') as file:
                return json.load(file)
        else:
            print(Fore.RED + f"No such file: {path}")
    except Exception as e:
        print(Fore.RED + f"An error occurred while loading the conversation: {str(e)}")

def main():
    print(Fore.GREEN + "\n=== Welcome to GPT-3.5 Chat ===" + Style.RESET_ALL)
    print("1. Set Assistant's Personality")
    print("2. Set Response Randomness (Temperature)")
    print("3. Start Chatting")
    print("4. Load Previous Conversation")
    print("5. Help")
    print("6. Exit")
    system_message = "You are an expert level code assistant who is extremely concise, helpful, and very wry."
    temperature = 0.5
    while True:
        conversation_history = [
            {
                "role": "system",
                "content": system_message
            }
        ]
        choice = input("\nChoose an option: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                system_message = input("Enter the system message for the assistant: ")
            elif choice == 2:
                temperature = float(input("Enter a temperature between 0 and 1: "))
            elif choice == 3:
                while True:
                    user_message = input(Fore.GREEN + "\nUser: " + Style.RESET_ALL)
                    if user_message.lower() in ['menu', 'exit', 'quit', 'stop']:
                        print(Fore.BLUE + "Chatbot: Goodbye!")
                        break
                    elif user_message.lower().startswith('open '):
                        path = user_message[5:]
                        python_code = load_python_file(path)
                        if python_code is not None:
                            user_message = python_code
                    elif user_message.lower() == 'save':
                        filename = input("Enter filename to save: ")
                        save_conversation(conversation_history, filename)
                        continue
                    elif user_message.lower() == 'help':
                        print(Fore.YELLOW + f"Current system message: {system_message}")
                        print(Fore.YELLOW + f"Current temperature: {temperature}")
                        continue
                    conversation_history.append({"role": "user", "content": user_message})
                    if len(''.join(msg['content'] for msg in conversation_history)) % TIME_BETWEEN_SYSTEM_MESSAGES < len(user_message):
                        conversation_history.append({"role": "system", "content": system_message})
                    finished = threading.Event()
                    loading_thread = threading.Thread(target=show_loading_animation, args=(finished,))
                    loading_thread.start()
                    response_message = call_openai_api(conversation_history, temperature)
                    finished.set()
                    print(Fore.CYAN + "GPT-3.5: ", end="")
                    print(Markdown(response_message))
                    conversation_history.append({"role": "assistant", "content": response_message})
                    if len(''.join(msg['content'] for msg in conversation_history)) > 3:
                        conversation_history = conversation_history[-10:]
            elif choice == 4:
                filename = input("Enter filename to load: ")
                loaded_conversation = load_conversation(filename)
                if loaded_conversation is not None:
                    conversation_history = loaded_conversation
                    system_message = [message["content"] for message in conversation_history if message["role"] == "system"][-1]
            elif choice == 5:
                print(Fore.YELLOW + "\n=== Help ===\n")
                print(Fore.YELLOW + "During a conversation:")
                print(Fore.YELLOW + "- Type 'menu', 'exit', 'quit', or 'stop' to return to the main menu.")
                print(Fore.YELLOW + "- Type 'save' to save the conversation to a text file.")
                print(Fore.YELLOW + "- Type 'open <file path>' to load a Python file.")
                print(Fore.YELLOW + "- Type 'help' to display the current system message (assistant's personality) and the")
                print(Fore.YELLOW + "  temperature (response randomness) setting.\n")
            elif choice == 6:
                return
            else:
                print(Fore.RED + "Invalid choice. Please choose 1, 2, 3, 4, 5, or 6.")
        else:
            print(Fore.RED + "Invalid input. Please enter a number.")

def load_python_file(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except Exception as e:
        print(Fore.RED + f"An error occurred while loading the Python file: {str(e)}")

if __name__ == "__main__":
    main()
