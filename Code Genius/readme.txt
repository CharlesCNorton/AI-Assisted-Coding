CodeGenius
CodeGenius is a Python program that utilizes artificial intelligence to generate new Python code or analyze and improve existing code. It leverages the OpenAI API to provide code generation, analysis, and enhancement capabilities. This program can be run from the command line and follows a series of prompts to guide the user through the process.

Prerequisites
Python 3.x
OpenAI API key
OpenAI organization name

Usage
Set your OpenAI API key and organization name in the openai.api_key and openai.organization variables in the code.
Run the program: python CodeGenius.py
Follow the prompts to choose whether to create a new program or analyze an existing one.
Provide the necessary input based on the chosen option.
The program will generate, analyze, and enhance the code iteratively based on AI responses.
At each iteration, you can choose to continue, save the code, or stop the process.
After completion, you can choose to restart the process or exit the program.

Example Usage
vbnet
Copy code
Python Code Generator and Analyzer

This program uses AI to either generate new Python code or analyze and improve existing code.
Please follow the prompts to proceed.

Create a new program or analyze an existing one? (new/existing): new

What code do you want me to write?: print("Hello, World!")

Processing initial request...
Initial code:
```python
print("Hello, World!")
Iteration...
Assistant's response:

python
Copy code
print("Hello, CodeGenius!")
Do you want to continue to the next step? (y/n): y

Iteration...
Assistant's response:

python
Copy code
print("Hello, CodeGenius!")
print("Welcome to the world of AI-powered coding!")
Do you want to continue to the next step? (y/n): s
Enter filename to save the code: hello.py

Do you want to restart the process? (y/n): n
Goodbye!

## License

This project is licensed under the AGPL-3.0 license.
