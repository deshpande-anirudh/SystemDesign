import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def consumer():
    stream_name = 'mystream'  # Name of the Redis stream

    # The last seen message ID (initially no message is seen)
    last_id = '0'  # '0' means starting from the very first message

    print(f"Listening to the stream: {stream_name}")

    while True:
        # XREAD command to read messages from the stream
        # The stream name and last seen ID is passed
        messages = redis_client.xread({stream_name: last_id}, count=1, block=0)

        for message in messages:
            # message[1] contains the actual message data (ID, fields)
            message_id, message_data = message[1][0]
            last_id = message_id  # Update last seen ID

            # Print the message
            print(f"Received message: {message_data}")
            print(f"Message ID: {message_id}")


if __name__ == "__main__":
    consumer()
