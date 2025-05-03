# Import required libraries
import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F

# Initialize model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Example documents
documents = [
    "Computer science is fascinating.",
    "I love playing football.",
    "Artificial Intelligence is the future.",
    "The match was exciting.",
    "Quantum computing will change the world."
]


# Function to embed text into embeddings
def embed(texts):
    """
    This function takes a list of texts, tokenizes them,
    and returns their embeddings using a pre-trained BERT model.

    Args:
    - texts (list of str): List of texts (e.g., sentences or documents).

    Returns:
    - torch.Tensor: A tensor containing the embeddings for the input texts.
    """
    # Tokenize texts
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

    # Get the model's output embeddings
    with torch.no_grad():
        model_output = model(**inputs)

    # Use mean pooling to get a single vector representation for each document
    # Mean pooling: average the embeddings of all tokens for each document
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings


# Function to search for the most similar documents based on a query
def search(query, documents, doc_embeddings):
    """
    This function computes the cosine similarity between the query and the documents,
    and returns the most similar documents.

    Args:
    - query (str): The search query.
    - documents (list of str): The list of documents to search within.
    - doc_embeddings (torch.Tensor): Embeddings for the documents.

    Returns:
    - None: Prints the most similar documents.
    """
    # Embed the query into the same embedding space as documents
    query_embedding = embed([query])

    # Compute cosine similarity between query and all document embeddings
    similarities = F.cosine_similarity(query_embedding, doc_embeddings)

    # Get the top 3 most similar documents
    topk = torch.topk(similarities, k=3)  # You can change k to get more/less results
    top_indices = topk.indices.tolist()

    # Print the top results
    print(f"Query: '{query}'\n")
    for idx in top_indices:
        print(f"Score: {similarities[idx]:.4f}")
        print(f"Document: {documents[idx]}")
        print()


# Main Execution
if __name__ == "__main__":
    # Embed all documents into vectors
    doc_embeddings = embed(documents)

    # Define a query for searching
    query = "AI will change everything"

    # Perform the search and print the top matching documents
    search(query, documents, doc_embeddings)
