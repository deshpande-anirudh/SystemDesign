import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load pre-trained GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')


# Function to generate text from GPT-2 model
def generate_text(prompt, max_length=5000):
    # Tokenize input prompt and return tensors
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    print(inputs)

    # Generate text using GPT-2 model
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, temperature=0.7)

    print(outputs[0])
    # Decode the generated output to text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_text


# Input prompt from the user
input_prompt = input("Enter your prompt: ")

# Generate output text
output_text = generate_text(input_prompt)

# Print the generated text
print("Generated Text: ", output_text)
