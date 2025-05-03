import re

def tokenize(text):
    # Convert text to lowercase
    text = text.lower()

    # Replace non-alphanumeric characters (except spaces) with spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # Split the text into tokens based on spaces
    tokens = text.split()

    return tokens


def advanced_tokenize(text):
    # Convert to lowercase
    text = text.lower()

    # Handle special cases: contractions (won't, isn't, etc.) and other common cases
    # Define a pattern for tokens (words, numbers, hashtags, mentions, etc.)
    token_pattern = r"\b(?:[a-z0-9]+(?:'?[a-z0-9]+)?|#\w+|@\w+|[.,!?;])\b"

    # Find all matching tokens based on the pattern
    tokens = re.findall(token_pattern, text)

    return tokens


# Example usage
text = "Hello, world! This is a test. #Python #Tokenization @user don't stop, won't stop!"
tokens = tokenize(text)
print(tokens)

adv_tokens = advanced_tokenize(text)
print(adv_tokens)
