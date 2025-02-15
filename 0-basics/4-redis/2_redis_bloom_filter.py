import redis
import random
import string

# Connect to Redis (make sure RedisBloom module is enabled)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Bloom filter key
bloom_filter_key = "emails"

# Create Bloom filter with a capacity of 1000 items and 0.01% false positive rate
redis_client.execute_command("BF.RESERVE", bloom_filter_key, 0.01, 1000)

# Function to generate random email-like strings
def generate_random_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com"

# Insert 1000 items into the Bloom filter
for i in range(1000):
    email = generate_random_email()
    redis_client.execute_command("BF.ADD", bloom_filter_key, email)

print("Inserted 1000 emails into the Bloom filter.")

# Check if 1000 items are present (simulate checking some emails)
for i in range(1000):
    email = generate_random_email()
    exists = redis_client.execute_command("BF.EXISTS", bloom_filter_key, email)
    print(f"Checking email '{email}': {'Exists' if exists else 'Does not exist'}")
