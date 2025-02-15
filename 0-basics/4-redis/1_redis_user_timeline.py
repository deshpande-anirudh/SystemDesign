import redis
import time

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


# Function to add a tweet to a user's timeline
def add_tweet(user_id: str, tweet_id: str, tweet_content: str):
    timestamp = time.time()
    tweet_data = f"{tweet_id}:{tweet_content}"
    redis_client.zadd(f"timeline:{user_id}", {tweet_data: timestamp})


# Function to get the latest tweets from a user's timeline
def get_timeline(user_id: str, count: int = 10):
    return redis_client.zrevrange(f"timeline:{user_id}", 0, count - 1)


# Example usage
user = "user123"
add_tweet(user, "tweet1", "Hello, world!")
add_tweet(user, "tweet2", "Redis is awesome!")

timeline = get_timeline(user)
print("User timeline:", timeline)
