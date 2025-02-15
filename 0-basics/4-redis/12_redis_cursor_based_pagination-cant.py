import redis
import time

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Function to add a tweet to a user's timeline
def add_tweet(user_id: str, tweet_id: str, tweet_content: str):
    try:
        timestamp = time.time()
        redis_client.zadd(f"timeline:{user_id}", {tweet_id: timestamp})
        redis_client.hset("tweets", tweet_id, tweet_content)
    except redis.RedisError as e:
        print(f"Error adding tweet: {e}")

# Function to get the latest tweets from a user's timeline with cursor-based pagination
def get_timeline(user_id: str, count: int = 10, cursor: int = 0):
    try:
        # Using zscan for cursor-based pagination
        # zscan returns a tuple of (cursor, data), where data is a list of (tweet_id, score) pairs
        new_cursor, tweet_data = redis_client.zscan(f"timeline:{user_id}", cursor=cursor, count=count)

        # tweet_data is a list of (tweet_id, score) tuples, so we need to extract tweet_ids
        tweet_ids = [tweet_id for tweet_id, _ in tweet_data]  # Extract tweet IDs from tuples

        # Manually limit the number of tweets to `count`
        if len(tweet_ids) > count:
            tweet_ids = tweet_ids[:count]  # Truncate to the desired count

        print(f"Fetched {len(tweet_ids)} tweet(s), Next cursor: {new_cursor}")  # Debug print

        if not tweet_ids:
            return [], new_cursor  # If no tweet IDs, return empty list and the same cursor

        # Fetch tweet contents in bulk
        tweets = redis_client.hmget("tweets", tweet_ids)

        # Filter out None values in case some tweets were deleted
        tweets = [tweet for tweet in tweets if tweet is not None]

        # Return the tweets along with the new cursor for pagination
        return tweets, new_cursor
    except redis.RedisError as e:
        print(f"Error fetching timeline: {e}")
        return [], cursor

# Example usage
user = "user123"

# Clear any existing data for this user (for testing purposes)
redis_client.delete(f"timeline:{user}")
redis_client.delete("tweets")

# Add 100 tweets to the user's timeline
for i in range(1, 101):
    add_tweet(user, f"tweet{i}", f"Tweet number {i}")

# Pagination: 10 tweets per page, starting from the first page
cursor = 0  # Cursor should be an integer, not a string
page = 1
tweets_per_page = 10

# Fetch pages
while True:
    tweets, cursor = get_timeline(user, count=tweets_per_page, cursor=cursor)
    if not tweets:
        break  # No more tweets, exit the loop
    print(f"Page {page}: {tweets}")  # Debug print
    page += 1
    if cursor == 0:  # Cursor is an integer, not a string
        break  # Exit loop if cursor is 0 (no more items to fetch)
    time.sleep(1)  # To simulate a small delay between page requests
