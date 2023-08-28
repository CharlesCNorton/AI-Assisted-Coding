# NeuraSum: Adaptive Document Summarizer

# Importing necessary libraries
import re
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class NeuraSum:

    @staticmethod
    def _tokenize_sentences(document: str) -> List[str]:
        """Tokenizes the document into sentences using regular expressions."""
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', document)
        return [sent.strip() for sent in sentences if sent]

    @staticmethod
    def _word_tokenize(document: str) -> List[str]:
        """Tokenizes the document into words using a simple delimiter-based approach."""
        return re.findall(r'\b\w+\b', document)

    @staticmethod
    def _compute_sentence_scores(document: str, sentences: List[str]) -> List[float]:
        """Computes the TF-IDF scores for each sentence in the document."""
        vectorizer = TfidfVectorizer(stop_words='english').fit([document])
        tfidf_matrix = vectorizer.transform(sentences)
        doc_vector = vectorizer.transform([document])
        cosine_similarities = linear_kernel(tfidf_matrix, doc_vector).flatten()
        return cosine_similarities

    @staticmethod
    def _extract_named_entities(document: str) -> List[str]:
        """Extracts named entities from the document using basic heuristics."""
        words = NeuraSum._word_tokenize(document)
        return [word for word in words if word[0].isupper()]

    @staticmethod
    def _prioritize_entities_in_summary(sentences: List[str], named_entities: List[str]) -> List[str]:
        """Prioritizes sentences containing named entities for inclusion in the summary."""
        entity_counts = [sum(sentence.count(entity) for entity in named_entities) for sentence in sentences]
        return [sent for _, sent in sorted(zip(entity_counts, sentences), reverse=True)]

    @staticmethod
    def _remove_redundancy(sentences: List[str]) -> List[str]:
        """Remove sentences that have overlapping information."""
        lowercase_sentences = [sent.lower() for sent in sentences]
        return [sentences[i] for i, sentence in enumerate(lowercase_sentences) if all(sentence not in other_sentence for j, other_sentence in enumerate(lowercase_sentences) if i != j)]

    @classmethod
    def summarize(cls, document: str, length: str = "medium") -> str:
        """Generate an adaptive length summary with prioritization of named entities."""
        length_percentage_map = {
            "short": 0.1,
            "medium": 0.2,
            "long": 0.3
        }

        num_sentences = int(len(cls._tokenize_sentences(document)) * length_percentage_map.get(length, 0.2))
        named_entities = cls._extract_named_entities(document)
        sentences = cls._tokenize_sentences(document)
        prioritized_sentences = cls._prioritize_entities_in_summary(sentences, named_entities)
        sentence_scores = cls._compute_sentence_scores(document, prioritized_sentences)
        ranked_sentences = [prioritized_sentences[i] for i in sentence_scores.argsort()[-num_sentences:][::-1]]
        non_redundant_sentences = cls._remove_redundancy(ranked_sentences)

        return " ".join(non_redundant_sentences[:num_sentences])


# Sample usage
sample_document = """
The Renaissance was a fervent period of European cultural, artistic, political and economic “rebirth” following the Middle Ages.
"""

NeuraSum.summarize(sample_document, "short")
