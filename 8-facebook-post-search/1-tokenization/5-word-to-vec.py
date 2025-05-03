from gensim.models import Word2Vec

# Tiny dataset
sentences = [
    ["I", "love", "eating", "an", "apple"],
    ["Apple", "released", "a", "new", "iPhone"]
]

# Train Word2Vec
model = Word2Vec(sentences, vector_size=5, min_count=1, window=3)

# Word vector
print("Word2Vec vector for 'apple':")
print(model.wv["apple"])  # or model.wv["Apple"] if you lowercase everything
