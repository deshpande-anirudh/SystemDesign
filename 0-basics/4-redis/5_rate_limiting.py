import redis
import time

# Create a Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Constants for rate limiting
RATE_LIMIT = 5  # Number of requests allowed per time window
TIME_WINDOW = 60  # Time window in seconds (e.g., 60 seconds = 1 minute)


def is_allowed(user_id):
    # Define the key that stores the request count for the user
    key = f"rate_limit:{user_id}"

    # Check the current request count
    current_count = redis_client.get(key)

    if current_count is None:
        # If the user doesn't have a key yet, this is their first request.
        # Set the key with an expiration time.
        redis_client.setex(key, TIME_WINDOW, 1)
        return True
    else:
        # If the user has already made requests, check if they're within the rate limit.
        if int(current_count) < RATE_LIMIT:
            # If they haven't exceeded the rate limit, increment the count.
            redis_client.incr(key)
            return True
        else:
            # If the user has exceeded the rate limit, reject the request.
            return False


def main():
    user_id = "user123"  # You can use any identifier for the user (e.g., IP address)

    # Simulate requests from the user
    for i in range(10):  # Simulate 10 requests
        if is_allowed(user_id):
            print(f"Request {i + 1} from {user_id} is allowed.")
        else:
            print(f"Request {i + 1} from {user_id} is denied due to rate limit.")
        time.sleep(5)  # Simulate a 5-second gap between requests


if __name__ == "__main__":
    main()
