Text Generator

This Python script leverages the Hugging Face transformers library to generate text using several language models including GPT-2 XL and custom LLAMA models.

Setup

Ensure you have the necessary Python libraries installed:

pip install torch transformers
The program uses local model files. Please make sure you have downloaded the necessary models to your local machine.

Usage

To run the program, navigate to the directory containing the text_generator.py file (or whatever you've named your Python script), and run:


python text_generator.py
This will start the text generator program and present you with a menu to either generate text or exit the program.

When you choose to generate text, you will be prompted to:

Choose a device for inferencing (cpu or cuda:0 for GPU).

Select the model you want to use for text generation.

Decide whether you want to use sequential execution (type yes or no).

Provide a prompt for text generation.
Specify the maximum length for the generated text.

Define the "temperature" of the output, which affects the randomness of the output.

After the text has been generated, you can choose to generate more text with the same model, change the model, or exit the program.