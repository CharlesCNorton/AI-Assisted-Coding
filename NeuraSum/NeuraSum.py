# NeuraSum: Advanced Document Summarizer

# Importing necessary libraries
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load Spacy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading the 'en_core_web_sm' model for Spacy (this may take a few moments)...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class NeuraSum:

    @staticmethod
    def _tokenize_sentences(document: str):
        """Tokenizes the document into sentences using Spacy."""
        doc = nlp(document)
        return [sent.text.strip() for sent in doc.sents]

    @staticmethod
    def _extract_named_entities(document: str):
        """Extracts named entities from the document using Spacy."""
        doc = nlp(document)
        return [ent.text for ent in doc.ents]

    @staticmethod
    def _compute_sentence_scores(sentences, document):
        """Computes the sentence scores based on TF-IDF and named entity emphasis."""
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(sentences + [document])
        cosine_sim = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])
        sentence_scores = cosine_sim.flatten()
        return sentence_scores

    @staticmethod
    def _rank_sentences(sentences, scores, num_sentences):
        """Ranks sentences based on their scores and returns the top sentences."""
        ranked_sentences = [sentences[i] for i in np.argsort(scores, axis=0)[::-1]]
        return ranked_sentences[:num_sentences]

    @staticmethod
    def _remove_redundancy(sentences):
        """Remove redundant sentences."""
        non_redundant_sentences = []
        for sentence in sentences:
            if not any(sentence in s for s in non_redundant_sentences):
                non_redundant_sentences.append(sentence)
        return non_redundant_sentences

    @classmethod
    def summarize(cls, document: str, length: str = "medium"):
        """Generate an adaptive length summary."""
        try:
            length_map = {"short": 0.1, "medium": 0.3, "long": 0.5}
            sentences = cls._tokenize_sentences(document)
            num_sentences = max(1, int(len(sentences) * length_map.get(length, 0.3)))
            sentence_scores = cls._compute_sentence_scores(sentences, document)
            ranked_sentences = cls._rank_sentences(sentences, sentence_scores, num_sentences * 2)
            non_redundant_sentences = cls._remove_redundancy(ranked_sentences)
            return ' '.join(non_redundant_sentences[:num_sentences])
        except Exception as e:
            return f"An error occurred: {e}"

# Sample usage
def main():
    print("Welcome to NeuraSum: Advanced Document Summarizer")
    sample_document = input("Please enter a document to summarize: ")
    length = input("Choose summary length (short, medium, long): ").lower()
    summary = NeuraSum.summarize(sample_document, length)
    print("\nSummary:")
    print(summary)

if __name__ == "__main__":
    main()