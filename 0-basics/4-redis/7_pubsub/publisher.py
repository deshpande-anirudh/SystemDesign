import redis
import time

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def publisher():
    # Channel to publish messages to
    channel = 'chat_channel'

    # Messages to be published
    messages = [
        "Hello, how are you?",
        "I am using Redis Pub/Sub!",
        "Redis Pub/Sub is awesome!",
        "Goodbye!"
    ]

    for message in messages:
        print(f"Publishing message: {message}")
        # Publish each message to the channel
        redis_client.publish(channel, message)
        time.sleep(2)  # Wait for 2 seconds before publishing the next message


if __name__ == "__main__":
    publisher()
