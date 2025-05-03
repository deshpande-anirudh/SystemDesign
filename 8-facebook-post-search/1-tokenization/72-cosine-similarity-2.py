import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def get_sentence_embedding(sentence):
    """
    Get the BERT embeddings for a sentence by averaging the token embeddings.
    """
    # Tokenize the sentence and get input IDs
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Get the BERT model output (last hidden state)
    with torch.no_grad():
        outputs = model(**inputs)

    # The last hidden state of shape (batch_size, sequence_length, hidden_size)
    last_hidden_states = outputs.last_hidden_state

    # We will take the mean of the embeddings across all tokens (including padding) to get a sentence-level representation
    sentence_embedding = last_hidden_states.mean(dim=1).squeeze()

    return sentence_embedding


# Sentences
sentence1 = "Apple released a new iPhone"
sentence2 = "I ate an apple"

# Get the sentence embeddings
embedding1 = get_sentence_embedding(sentence1)
embedding2 = get_sentence_embedding(sentence2)

# Calculate cosine similarity between the two sentence embeddings
similarity = cosine_similarity([embedding1.numpy()], [embedding2.numpy()])

print(f"Cosine Similarity between the sentences: {similarity[0][0]}")


sentence1 = "Apple released a new iPhone"
sentence2 = "Apple's iPhone 17"

# Get the sentence embeddings
embedding1 = get_sentence_embedding(sentence1)
embedding2 = get_sentence_embedding(sentence2)

# Calculate cosine similarity between the two sentence embeddings
similarity = cosine_similarity([embedding1.numpy()], [embedding2.numpy()])

print(f"Cosine Similarity between the sentences: {similarity[0][0]}")


sentence1 = "Apple is Red"
sentence2 = "Apple is sweet and delicious"

# Get the sentence embeddings
embedding1 = get_sentence_embedding(sentence1)
embedding2 = get_sentence_embedding(sentence2)

# Calculate cosine similarity between the two sentence embeddings
similarity = cosine_similarity([embedding1.numpy()], [embedding2.numpy()])

print(f"Cosine Similarity between the sentences: {similarity[0][0]}")
