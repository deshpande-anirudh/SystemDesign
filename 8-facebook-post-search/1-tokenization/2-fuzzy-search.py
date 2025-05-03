from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Example words to compare
word = "tokenization"
word_list = ["tokenize", "token", "tokenized", "toking", "recognization"]

# Calculate similarity ratio
for w in word_list:
    ratio = fuzz.ratio(word, w)
    print(f"Similarity between '{word}' and '{w}': {ratio}%")

# Use process.extractOne to find the best match
best_match = process.extractBests(word, word_list)
print(f"Best match for '{word}': {best_match}")
