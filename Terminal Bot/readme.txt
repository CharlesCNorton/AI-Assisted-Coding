#TerminalBot

This is a Python script for a console chat application that uses OpenAI's GPT-3.5 Turbo model to generate responses to user input. The script also includes features such as loading and saving conversations, adjusting the temperature of the model, and toggling multi-turn conversations and text-to-speech.

Dependencies:
os
openai
json
pyttsx3
re
markdown2
rich
asyncio
atexit
functools

Usage

To run the script, simply execute the TerminalBot.py file in a Python environment. The script will prompt the user for input and generate responses using the GPT-3.5 Turbo model.

The script includes several commands that can be used to adjust its behavior:

multi: toggles multi-turn conversations on or off
set temperature X: sets the temperature of the model to a value between 0 and 1
set system message: changes the system message displayed at the start of the conversation
load path/to/file: loads the contents of a file and displays them in the console
clear history: clears the conversation history
save conversation [filename]: saves the conversation history to a file
toggle tts: toggles text-to-speech on or off
quit, exit, or bye: exits the script