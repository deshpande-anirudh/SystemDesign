import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def subscriber():
    # Channel to subscribe to
    channel = 'chat_channel'

    # Create a pubsub object to listen to Redis messages
    pubsub = redis_client.pubsub()

    # Subscribe to the channel
    pubsub.subscribe(channel)

    print(f"Subscribed to {channel}. Waiting for messages...")

    # Listen for messages indefinitely
    for message in pubsub.listen():
        # Each message is a dictionary
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")


if __name__ == "__main__":
    subscriber()
