import torch
import torch.nn as nn
from transformers import GPT2Tokenizer
from datasets import load_dataset
from torch.utils.data import DataLoader, Dataset

# Step 1: Load and Preprocess the Dataset
dataset = load_dataset('wikitext', 'wikitext-103-raw-v1', split='train[:1%]')  # Load a small portion for quick training

# Initialize GPT2 tokenizer (subword tokenization)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], return_tensors="pt", truncation=True, padding="max_length", max_length=128)


tokenized_dataset = dataset.map(tokenize_function, batched=True)


# Step 2: Build the GPT Model (Simple GPT architecture)
class SimpleGPT(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads):
        super(SimpleGPT, self).__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.transformer_blocks = nn.ModuleList([
            nn.TransformerDecoderLayer(d_model=hidden_size, nhead=num_heads) for _ in range(num_layers)
        ])
        self.fc_out = nn.Linear(hidden_size, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        for block in self.transformer_blocks:
            x = block(x, x)  # Using self-attention
        return self.fc_out(x)


# Step 3: Set Hyperparameters and Initialize Model
vocab_size = len(tokenizer)
hidden_size = 256  # Dimensionality of the embeddings
num_layers = 2  # Number of transformer layers
num_heads = 4  # Number of attention heads

# Instantiate the model
model = SimpleGPT(vocab_size, hidden_size, num_layers, num_heads)

# Step 4: Define Training Loop
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the optimizer and loss function
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)
criterion = nn.CrossEntropyLoss()


# DataLoader
class TextDataset(Dataset):
    def __init__(self, tokenized_data):
        self.data = tokenized_data["input_ids"]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return torch.tensor(self.data[idx])


train_data = TextDataset(tokenized_dataset)
train_loader = DataLoader(train_data, batch_size=4, shuffle=True)

# Training loop
num_epochs = 3
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in train_loader:
        batch = batch.to(device)

        # Create shifted labels for next-token prediction
        labels = batch.clone().detach()
        outputs = model(batch)

        # Calculate loss
        loss = criterion(outputs.view(-1, vocab_size), labels.view(-1))
        total_loss += loss.item()

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss / len(train_loader)}")


# Step 5: Generate Text (Testing)
def generate_text(prompt, max_length=50):
    model.eval()
    inputs = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    generated = inputs

    for _ in range(max_length):
        outputs = model(generated)
        predictions = outputs[:, -1, :]
        next_token = predictions.argmax(dim=-1)
        generated = torch.cat((generated, next_token.unsqueeze(-1)), dim=-1)

    return tokenizer.decode(generated[0], skip_special_tokens=True)
M

# Test with a prompt
prompt = "Once upon a time"
generated_text = generate_text(prompt)
print(f"Generated Text: {generated_text}")
