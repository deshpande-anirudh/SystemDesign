from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Input sentence
sentence = "I ate an apple"
inputs = tokenizer(sentence, return_tensors="pt")

print(inputs)

# Get BERT output
outputs = model(**inputs)

# Hidden states of each token
last_hidden_state = outputs.last_hidden_state

# Find the vector for 'apple'
apple_token_index = inputs.input_ids[0].tolist().index(tokenizer.convert_tokens_to_ids("apple"))
apple_vector = last_hidden_state[0, apple_token_index]

print("BERT vector for 'apple' in sentence:")
print(apple_vector)

sentence2 = "Apple released a new iPhone"
inputs = tokenizer(sentence, return_tensors="pt")


# I want to get cosine similarity between apple in --- Apple released a new iPhone and I ate an apple


