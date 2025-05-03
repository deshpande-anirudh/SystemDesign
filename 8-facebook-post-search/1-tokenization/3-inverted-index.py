import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from sklearn.datasets import fetch_20newsgroups
import string
from collections import defaultdict

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')


class TextSearch:
    def __init__(self, dataset_size=1000):
        # Load data
        newsgroups = fetch_20newsgroups(subset='train')
        self.documents = newsgroups.data[:dataset_size]  # Limit to first `dataset_size` documents

        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer()

        # Create inverted index
        self.inverted_index = defaultdict(set)
        self._build_inverted_index()

    def get_wordnet_pos(self, treebank_tag):
        """Convert POS tag format from NLTK to WordNet format"""
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        return wordnet.NOUN  # Default to noun

    def preprocess(self, text):
        """Preprocess text: lowercase, remove punctuation, stopwords, tokenize, lemmatize"""
        text = text.lower()
        stop_words = set(stopwords.words('english'))
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in stop_words]
        pos_tags = pos_tag(tokens)

        # Lemmatize tokens based on POS tags
        return [
            self.lemmatizer.lemmatize(word, self.get_wordnet_pos(pos))
            for word, pos in pos_tags
            if word.isalpha()  # Keep only alphabetic words
        ]

    def _build_inverted_index(self):
        """Build inverted index from documents"""
        for doc_id, text in enumerate(self.documents):
            tokens = self.preprocess(text)
            for token in tokens:
                self.inverted_index[token].add(doc_id)

    def search(self, query):
        """Search for documents containing all query terms"""
        query_tokens = self.preprocess(query)
        result_docs = None
        for token in query_tokens:
            if token in self.inverted_index:
                if result_docs is None:
                    result_docs = self.inverted_index[token].copy()
                else:
                    result_docs &= self.inverted_index[token]  # AND search
            else:
                result_docs = set()  # No matches if token is not found
                break
        return sorted(result_docs) if result_docs else []

    def print_search_results(self, query):
        """Print documents that match the search query"""
        search_results = self.search(query)
        if search_results:
            print(f"Documents containing '{query}': {search_results}")
            doc_id = random.choice(search_results)
            print(f"\nDocument {doc_id}:\n{self.documents[doc_id]}")
        else:
            print("No documents found matching the query.")


# Example usage
text_search = TextSearch()

query = "computer science"
text_search.print_search_results(query)
