# Import required libraries
import torch
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
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
    """Embed text into embeddings using a pre-trained BERT model"""
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**inputs)
    embeddings = model_output.last_hidden_state.mean(dim=1)  # Mean pooling
    return embeddings


# Function to visualize cosine similarity between documents and a query
# Function to visualize cosine similarity between documents and a query
def visualize_similarity(query, documents, doc_embeddings):
    """
    Visualizes the cosine similarity between the query and documents using t-SNE.
    Displays a scatter plot with the query and documents plotted in 2D space.
    """
    # Embed the query
    query_embedding = embed([query])

    # Compute cosine similarity between query and document embeddings
    similarities = F.cosine_similarity(query_embedding, doc_embeddings)

    # Prepare embeddings for visualization
    all_embeddings = torch.cat([query_embedding, doc_embeddings], dim=0).cpu().numpy()

    # Apply t-SNE to reduce to 2D space
    tsne = TSNE(n_components=2, perplexity=3, random_state=42)  # Set perplexity to a lower value
    reduced_embeddings = tsne.fit_transform(all_embeddings)

    # Plot the t-SNE projection
    plt.figure(figsize=(8, 6))
    plt.scatter(reduced_embeddings[1:, 0], reduced_embeddings[1:, 1], color='blue', label='Documents', s=100)
    plt.scatter(reduced_embeddings[0, 0], reduced_embeddings[0, 1], color='red', label='Query', s=200, marker='X')

    # Annotate the documents
    for i, doc in enumerate(documents):
        plt.annotate(f'Doc {i + 1}', (reduced_embeddings[i + 1, 0], reduced_embeddings[i + 1, 1]), fontsize=12)

    plt.title(f"Cosine Similarity: Query vs Documents", fontsize=16)
    plt.legend(loc='best')
    plt.show()

# Main Execution
if __name__ == "__main__":
    # Embed all documents into vectors
    doc_embeddings = embed(documents)

    # Define a query for searching
    query = "AI will change everything"

    # Visualize the similarity between query and documents
    visualize_similarity(query, documents, doc_embeddings)
