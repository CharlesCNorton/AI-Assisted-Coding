LoraMerge

LoraMerge is a comprehensive tool designed to merge PEFT adapters with base models. The user-friendly terminal menu and the intuitive GUI directory selection make the model merging process streamlined and straightforward.

Deep Acknowledgment: We owe a tremendous debt of gratitude to TheBloke for the original script that served as a cornerstone for this project. TheBloke's script can be found at: https://gist.github.com/TheBloke/d31d289d3198c24e0ca68aaf37a19032. Recognizing the complexities involved in merging models, this repository was born out of a necessity. It is our ardent wish that LoraMerge simplifies the model merging journey for many. Once again, thank you, TheBloke, for lighting the path.


Practical Usage
Upon starting LoraMerge, you are greeted with a terminal-based menu:

========= LoraMerge: Merge PEFT Adapters with a Base Model =========

Based on an original script by TheBloke available at:
https://gist.github.com/TheBloke/d31d289d3198c24e0ca68aaf37a19032

Options:
1. Merge models
2. Acknowledgment & Citation
3. Exit
Menu Layout & Functions:

Merge models: This option commences the model merging process.

First, a GUI dialog prompts you to select the directory of the pretrained base model.
Next, you're guided to choose the directory for the PEFT model.
Finally, specify the output directory where the merged model will be saved.
The merging process starts, and upon completion, a confirmation message with the output directory path is shown.
Acknowledgment & Citation: A heartfelt acknowledgment and citation for TheBloke is displayed.

Exit: Exits the program.

The GUI-based directory selections are intuitive, and in case of any hiccups or unintentional cancellations, the program provides meaningful error messages guiding you forward.

Technical Usage
To start LoraMerge:

Clone the repository:

git clone <repository_url>
Navigate to the directory:

bash
Copy code
cd <repository_directory>
Run the program:

python LoraMerge.py [--device <device_name>]
Parameters:

--device: Specifies the device for model loading, such as 'cuda:0' or 'cpu'. By default, it's set to 'auto', which auto-selects the available device.

License: GNU Affero General Public License v3.0 as per TheBloke.
