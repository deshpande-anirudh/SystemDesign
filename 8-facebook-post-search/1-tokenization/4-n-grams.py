import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from sklearn.datasets import fetch_20newsgroups
import string
from collections import defaultdict
from nltk.util import ngrams

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')


class TextSearch:
    def __init__(self, dataset_size=1000, ngram_range=(1, 2)):
        """
        Initialize the TextSearch object.

        :param dataset_size: Number of documents to load from the dataset
        :param ngram_range: Tuple indicating the range of n-grams (min_n, max_n)
        """
        # Load data
        newsgroups = fetch_20newsgroups(subset='train')
        self.documents = newsgroups.data[:dataset_size]  # Limit to first `dataset_size` documents

        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer()

        # Set the n-gram range (e.g., (1, 2) for unigrams and bigrams)
        self.ngram_range = ngram_range

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
        lemmatized_tokens = [
            self.lemmatizer.lemmatize(word, self.get_wordnet_pos(pos))
            for word, pos in pos_tags
            if word.isalpha()  # Keep only alphabetic words
        ]

        return lemmatized_tokens

    def generate_ngrams(self, tokens):
        """Generate n-grams from tokenized text."""
        all_ngrams = []
        for n in range(self.ngram_range[0], self.ngram_range[1] + 1):
            all_ngrams.extend(ngrams(tokens, n))  # Generate n-grams of size n
        return [' '.join(gram) for gram in all_ngrams]  # Join n-grams as strings

    def _build_inverted_index(self):
        """Build inverted index from documents"""
        for doc_id, text in enumerate(self.documents):
            tokens = self.preprocess(text)
            ngrams_list = self.generate_ngrams(tokens)

            # Debug: print n-grams generated for each document
            print(f"Document {doc_id} N-grams: {ngrams_list}")

            for ngram in ngrams_list:
                self.inverted_index[ngram].add(doc_id)

        # Debug: print the inverted index
        print("\nInverted Index:")
        for ngram, docs in self.inverted_index.items():
            print(f"{ngram}: {docs}")

    def search(self, query):
        """Search for documents containing all query terms (n-grams)"""
        query_tokens = self.preprocess(query)
        query_ngrams = self.generate_ngrams(query_tokens)

        # Debug: print query n-grams
        print(f"Query n-grams: {query_ngrams}")

        result_docs = None
        for ngram in query_ngrams:
            if ngram in self.inverted_index:
                if result_docs is None:
                    result_docs = self.inverted_index[ngram].copy()
                else:
                    result_docs &= self.inverted_index[ngram]  # AND search
            else:
                result_docs = set()  # No matches if n-gram is not found
                break

        # Debug: print result docs
        print(f"Result docs: {result_docs}")

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
text_search = TextSearch(ngram_range=(1, 2))  # Using unigrams and bigrams

query = "computer science is great"
text_search.print_search_results(query)
