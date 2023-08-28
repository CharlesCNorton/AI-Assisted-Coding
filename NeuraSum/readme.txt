NeuraSum: Adaptive Document Summarizer
--------------------------------------

Description:
------------
NeuraSum is an extractive document summarizer designed to generate concise summaries from larger texts. It prioritizes named entities and adjusts the length of the summary based on user preference. NeuraSum is built using traditional natural language processing techniques and is designed for modularity and future expansion.

Features:
---------
1. Extractive Summarization: Selects the most informative sentences from the source document to create a summary.
2. Named Entity Recognition: Prioritizes sentences containing named entities to make summaries more informative.
3. Adaptive Length: Adjusts the summary length based on a percentage of the total number of sentences in the document.

Usage:
------
from NeuraSum import NeuraSum

# Your document to summarize
document = "Your long text here..."

# Generate a medium-length summary
summary = NeuraSum.summarize(document, "medium")
print(summary)

Dependencies:
-------------
- Python 3.x
- scikit-learn

Contributions:
--------------
Contributions are welcome! Please fork the repository and submit a pull request with your changes.