LinguaLens: Dataset Examination Tool
------------------------------------

LinguaLens is designed as an intuitive tool for users who wish to analyze the symmetry of text datasets, especially when preparing data for fine-tuning language models. The primary goal of LinguaLens is to provide a clear and concise overview of a dataset's structural composition.

When a dataset is loaded into LinguaLens, the application parses through the sentences and performs two primary categorizations:

First, it evaluates the length of sentences, segmenting them into groups labeled as Short, Medium, Large, or Other. This segmentation helps users quickly gauge the distribution of sentence lengths in their datasets.

Second, it examines the punctuation that concludes each sentence, specifically looking for question marks, periods, and exclamation points. By doing so, LinguaLens classifies sentences as Questions, Statements, or Exclamations. This can offer insights into the tonality and intent distribution within the dataset.

Additionally, the application provides a summarized view of the analysis, which is especially useful for quickly understanding the dataset's balance and structure. For those who may be new to the tool or require a deeper understanding of the categorizations, LinguaLens features an integrated Help section. This section explains the methodology of analysis and provides guidelines on using the application.

To use LinguaLens, follow these steps:
- Launch the `lingualens.py` application.
- Navigate to the File menu and select a .txt file for analysis.
- The results will be immediately displayed in the main application window.

The idea behind LinguaLens is to empower users, from data scientists to language enthusiasts, to better understand and prepare their text datasets. By offering insights into sentence structures and tonal distributions, we believe LinguaLens can be an indispensable tool in the preprocessing steps of language model training.