import redis
import time

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Function to add a tweet to a user's timeline
def add_tweet(user_id: str, tweet_id: str, tweet_content: str):
    timestamp = time.time()
    redis_client.zadd(f"timeline:{user_id}", {tweet_id: timestamp})
    redis_client.hset("tweets", tweet_id, tweet_content)

# Function to get the latest tweets from a user's timeline
def get_timeline(user_id: str, count: int = 10):
    tweet_ids = redis_client.zrevrange(f"timeline:{user_id}", 0, count - 1)
    return redis_client.hmget("tweets", tweet_ids)

# Example usage
user = "user123"
add_tweet(user, "tweet1", "Hello, world!")
add_tweet(user, "tweet2", "Redis is awesome!")

timeline = get_timeline(user)
print("User timeline:", timeline)
