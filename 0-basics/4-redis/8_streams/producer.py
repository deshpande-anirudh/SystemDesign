import redis
import time

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def producer():
    stream_name = 'mystream'  # Name of the Redis stream

    # Sample messages
    messages = [
        {"user": "alice", "message": "Hello, world!"},
        {"user": "bob", "message": "Hi, everyone!"},
        {"user": "carol", "message": "How's it going?"},
        {"user": "dave", "message": "Goodbye!"}
    ]

    for msg in messages:
        # XADD command to add a message to the stream
        print(f"Adding message to stream: {msg}")
        redis_client.xadd(stream_name, msg)
        time.sleep(2)  # Simulating some delay between message sending


if __name__ == "__main__":
    producer()
