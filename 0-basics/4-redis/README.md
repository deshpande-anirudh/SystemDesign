# What is REDIS? 

It is a key-value ["data structure store"](https://redis.io/about/). 

**Keys**:

Redis keys must be **binary-safe strings** (i.e., sequences of bytes). This means:  

1. **They can contain any characters**, including spaces, newlines, and binary data.  
2. **They have a maximum length** of **512 MB**, 
   1. but practically keep it less than 100 bytes (100 characters).  
3. **They are case-sensitive** (e.g., `"key1"` and `"Key1"` are different).  

However, keys **cannot** be of types like lists, sets, or hashes—those are **values** stored under a string key.

**Values**: 

Also **have a maximum length** of **512 MB**.

Can be of type - 

- Strings
- Hashes (Objects)
- Lists
- Sets
- Sorted Sets (Priority Queues)
- Bloom Filters
- Geospatial Indexes
- Time Series

## Key naming patterns to avoid hot-keys

For better scaling in Redis, structuring keys efficiently is crucial. Here are some best practices:  

### 1. **Use a Consistent Naming Pattern**  
A structured naming convention makes debugging and querying easier. A common pattern:  
   ```
   <namespace>:<type>:<id>:<attribute>
   ```
   Example:  
   ```
   user:profile:123:name → "John Doe"
   order:2025-02-13:987 → "{...order details...}"
   ```

### 2. **Avoid Hot Keys**  
- Distribute frequently accessed data across multiple keys to avoid overwhelming a single key.  
- Example: Instead of one key `hot_articles`, use `hot_articles:shard1`, `hot_articles:shard2`, etc.  

### 3. **Leverage Hashes for Small Items**  
Instead of storing multiple small keys, use a hash:  
   ```  
   HMSET user:123 name "Alice" age 30 country "US"  
   ```
   This reduces memory overhead and improves lookup efficiency.  

### 4. **Use Logical Sharding in Keys**  
If using **Redis Cluster**, distribute keys across nodes with consistent hashing:  
   ```
   user:{123}:profile → Ensures data stays in the same slot
   ```
   Curly braces `{}` indicate a **hash tag** to keep related keys together.  

### 5. **Time-based Keys for Expiring Data**  
For logs, leaderboards, or time-sensitive data, append timestamps:  
   ```
   logs:2025-02-13:1234
   ```
   Use `EXPIRE` or `TTL` to auto-delete old data.  

### 6. **Minimize Key Cardinality in High-Traffic Scenarios**  
Instead of  
   ```
   click:user:123:buttonA
   click:user:123:buttonB
   ```
Store all clicks in a single hash or sorted set:  
   ```
   HINCRBY click:user:123 buttonA 1
   ```

### 7. **Use Sorted Sets for Ranking and Queues**  
For leaderboards or priority queues:  
   ```
   ZADD leaderboard 5000 "player1"
   ZADD leaderboard 6000 "player2"
   ```

### 8. **Optimize for Scan Operations**  
If you need to scan keys efficiently, use a prefix:  
   ```
   session:active:<id> 
   ```
   Then use `SCAN 0 MATCH session:active:*` for efficient iteration.  

### 9. **Compress Large Keys and Values**  
- Store compressed JSON (e.g., using MessagePack) to save memory.  
- Example: Instead of storing a large JSON string, use `msgpack` or `protobuf`.  

### 10. **Monitor and Adjust**  
Use `redis-cli` or `MONITOR` to analyze access patterns and adjust key structures as needed.

# Common commands

Here's a table of common Redis commands for each of the mentioned data types:

| **Data Type**             | **Command**                                 | **Description**                                                                 |
|---------------------------|---------------------------------------------|---------------------------------------------------------------------------------|
| **Strings**               | `SET key value`                             | Set the value of a key.                                                          |
|                           | `GET key`                                   | Get the value of a key.                                                          |
|                           | `INCR key`                                  | Increment the integer value of a key.                                            |
|                           | `DECR key`                                  | Decrement the integer value of a key.                                            |
|                           | `MSET key1 value1 key2 value2 ...`          | Set multiple keys to multiple values.                                            |
|                           | `MGET key1 key2 ...`                        | Get the values of multiple keys.                                                 |
|                           | `SETEX key seconds value`                   | Set a key’s value and expire it after a given number of seconds.                 |
|                           | `APPEND key value`                          | Append a value to the end of a key’s value.                                      |
| **Hashes (Objects)**      | `HSET hash field value`                     | Set the value of a hash field.                                                   |
|                           | `HGET hash field`                           | Get the value of a hash field.                                                   |
|                           | `HGETALL hash`                              | Get all fields and values in a hash.                                             |
|                           | `HDEL hash field`                           | Delete one or more fields in a hash.                                             |
|                           | `HINCRBY hash field increment`              | Increment the integer value of a hash field.                                    |
|                           | `HKEYS hash`                                | Get all the field names in a hash.                                               |
|                           | `HVALS hash`                                | Get all the values in a hash.                                                    |
| **Lists**                 | `LPUSH list value`                          | Prepend one or more values to a list.                                            |
|                           | `RPUSH list value`                          | Append one or more values to a list.                                             |
|                           | `LPOP list`                                 | Remove and get the first element of a list.                                      |
|                           | `RPOP list`                                 | Remove and get the last element of a list.                                       |
|                           | `LRANGE list start stop`                    | Get a range of elements from a list.                                             |
|                           | `LLEN list`                                 | Get the length of a list.                                                       |
|                           | `LREM list count value`                     | Remove elements from a list.                                                     |
| **Sets**                  | `SADD set member`                           | Add one or more members to a set.                                               |
|                           | `SMEMBERS set`                              | Get all members of a set.                                                       |
|                           | `SISMEMBER set member`                      | Check if a member is in a set.                                                  |
|                           | `SREM set member`                           | Remove one or more members from a set.                                          |
|                           | `SCARD set`                                 | Get the number of members in a set.                                             |
|                           | `SUNION set1 set2 ...`                      | Get the union of multiple sets.                                                 |
|                           | `SINTER set1 set2 ...`                      | Get the intersection of multiple sets.                                          |
| **Sorted Sets (Priority Queues)** | `ZADD zset score member`                  | Add one or more members to a sorted set, or update the score of an existing member. |
|                           | `ZREM zset member`                          | Remove one or more members from a sorted set.                                   |
|                           | `ZRANGE zset start stop`                    | Get a range of members in a sorted set.                                         |
|                           | `ZREVRANGE zset start stop`                 | Get a range of members in a sorted set, ordered from highest to lowest score.   |
|                           | `ZSCORE zset member`                        | Get the score of a member in a sorted set.                                      |
|                           | `ZCARD zset`                                | Get the number of members in a sorted set.                                      |
|                           | `ZCOUNT zset min max`                       | Count the number of members in a sorted set with scores within a range.         |
| **Bloom Filters**         | `BF.ADD key item`                           | Add an item to the Bloom filter.                                                 |
|                           | `BF.EXISTS key item`                        | Check if an item exists in the Bloom filter.                                    |
|                           | `BF.MADD key item1 item2 ...`                | Add multiple items to the Bloom filter.                                         |
|                           | `BF.MEXISTS key item1 item2 ...`             | Check multiple items' existence in the Bloom filter.                            |
| **Geospatial Indexes**    | `GEOADD key longitude latitude member`       | Add a geospatial item (latitude, longitude) to a sorted set.                    |
|                           | `GEODIST key member1 member2`               | Get the distance between two members in a geospatial index.                      |
|                           | `GEOPOS key member`                         | Get the position (longitude, latitude) of a member in a geospatial index.       |
|                           | `GEORADIUS key longitude latitude radius`    | Get all members within a radius from a point in a geospatial index.              |
|                           | `GEORADIUSBYMEMBER key member radius`       | Get all members within a radius from a member in a geospatial index.             |
| **Time Series**           | `TS.ADD key timestamp value`                 | Add a data point to a time series.                                               |
|                           | `TS.MADD key timestamp value ...`            | Add multiple data points to a time series.                                      |
|                           | `TS.RANGE key from_timestamp to_timestamp`   | Get the range of data points in a time series within a given time range.        |
|                           | `TS.INCRBY key timestamp value`              | Increment the value of a time series by a given amount at a given timestamp.     |
|                           | `TS.DEL key from_timestamp to_timestamp`     | Delete data points within a given time range in a time series.                  |
|                           | `TS.CREATIONTIME key`                       | Get the creation time of a time series.                                         |

These are the basic commands to get started with each Redis data type. Let me know if you need more detailed examples or specific use cases!

# REDIS as a cache

Store a precomputed user timeline in Redis using a sorted set (ZSET). Each user's timeline can be stored as a sorted set where:

 - The score is the timestamp of the tweet (to keep it sorted chronologically).
 - The value is the tweet ID or JSON representation of the tweet.

```python
def add_tweet(user_id: str, tweet_id: str, tweet_content: str):
    timestamp = time.time()
    tweet_data = f"{tweet_id}:{tweet_content}"
    redis_client.zadd(f"timeline:{user_id}", {tweet_data: timestamp})


# Function to get the latest tweets from a user's timeline
def get_timeline(user_id: str, count: int = 10):
    return redis_client.zrevrange(f"timeline:{user_id}", 0, count - 1)
```

## Structuring keys (for billions of keys)

For **billions of users**, your key structure and storage efficiency matter.  

### Issues with `f"{tweet_id}:{tweet_content}"` as a value:
1. **Redundant Data**: Storing full tweet content inside the timeline wastes space. The same tweet might be stored for multiple users.
2. **Limited Lookup**: You can't easily fetch tweet details separately.
3. **Key Size Growth**: Tweet content varies in length, making timelines unpredictable in size.

### **Better Alternative: Store Only `tweet_id`**
Instead of `f"{tweet_id}:{tweet_content}"`, store **just the tweet ID** in the sorted set:

```python
redis_client.zadd(f"timeline:{user_id}", {tweet_id: timestamp})
```

Then, store actual tweet content **separately** in a Redis `HASH` or a database:

```python
redis_client.hset("tweets", tweet_id, tweet_content)
```

### **Benefits of this approach:**
✅ **Efficient Storage** – Avoids duplication of tweet content across user timelines.  
✅ **Faster Access** – Redis handles numerical IDs better than long strings.  
✅ **Scalability** – Easier to shard across multiple Redis instances.  
✅ **Flexibility** – You can update tweet content without modifying timelines.  

### **Retrieving the Timeline:**
1. Get tweet IDs from the timeline:
   ```python
   tweet_ids = redis_client.zrevrange(f"timeline:{user_id}", 0, count - 1)
   ```
2. Fetch tweet content separately:
   ```python
   tweets = redis_client.hmget("tweets", tweet_ids)
   ```

# Redlock (distributed lock)

In your Redlock implementation, multiple Redis instances are needed to follow the Redlock algorithm, which is designed for **distributed locking** in environments with multiple, potentially unreliable, Redis nodes. Here’s why multiple instances are required:

### 1. **Fault Tolerance**:
   Redlock aims to handle the case where one Redis instance goes down. By having multiple Redis instances (typically 5 or more in a production environment), the algorithm ensures that the lock is still available even if some nodes are unavailable. The distributed system can tolerate a few failures without losing the ability to acquire the lock.

### 2. **Safety and Reliability**:
   The key idea of Redlock is to ensure that a lock is only granted if **a majority** of the Redis nodes successfully acquire the lock. If one or two instances are down, the lock cannot be granted, preventing situations where a lock is granted but the system is not in a consistent state.

   The steps of the algorithm are:
   - **Step 1**: The client tries to acquire the lock in multiple Redis instances.
   - **Step 2**: It ensures that the lock is acquired in at least a **majority** of Redis instances. If so, the lock is considered acquired.
   - **Step 3**: If the lock is not acquired in a majority of the nodes, the client must release any locks it might have obtained and retry, ensuring consistency across nodes.

### 3. **Ensuring a Stronger Guarantee**:
   In distributed systems, single-node failures are inevitable. If you were to use only a single Redis instance (or even just two instances), the system wouldn't be fault-tolerant because, if that instance becomes unavailable, your lock system would fail. By using multiple nodes, you significantly reduce the risk of lock contention or system failure.

### 4. **Performance Considerations**:
   With multiple Redis instances, you can distribute the load of acquiring locks and handling requests, which improves performance in high-traffic systems. Each Redis instance can handle a portion of the requests, making the entire system more scalable.

### Typical Configuration:
   - In a real-world Redlock setup, you would have **odd-numbered Redis instances** (usually 5 or 7) across different servers or containers. This way, the majority of nodes (i.e., 3 out of 5 or 4 out of 7) can be considered when acquiring the lock.

In summary, the **multiple Redis instances** provide:
- **Fault tolerance** and **resilience** to node failures.
- **Consistency** by requiring the lock to be acquired by a majority.
- **Better performance** under load.

# Redis streams (pubsub with persistence)

Sure! Redis Streams is a data structure that allows you to work with real-time message queues. It’s similar to Pub/Sub, but with a few important differences. Redis Streams provide more advanced features like message persistence, message IDs, and consumer groups, which makes it well-suited for building distributed systems and message processing pipelines.

Below is a simple example of using Redis Streams with `redis-py`. This example demonstrates how to **add messages to a Redis stream** and how to **consume messages from that stream**.

### Requirements:
- `redis-py` library (Python Redis client)

You can install it via pip:
```bash
pip install redis
```

### Redis Streams Example

#### Producer Code (Writing to the Stream):
This code simulates a producer adding messages to a Redis stream.

```python
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
```

#### Consumer Code (Reading from the Stream):
This code simulates a consumer that reads messages from the Redis stream.

```python
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
```

### How This Works:
1. **Producer**:
   - The producer generates some sample messages (e.g., user messages) and adds them to the stream using `xadd(stream_name, message)`. 
   - Each message is added with a unique ID (auto-generated by Redis) and can contain multiple fields (e.g., `user` and `message`).
   
2. **Consumer**:
   - The consumer reads from the stream using `xread({stream_name: last_id}, count=1, block=0)`. 
   - It blocks and waits for new messages to arrive in the stream. When a new message arrives, it processes the message and prints it.
   - The `last_id` keeps track of the last message ID that the consumer has processed, so it can fetch only new messages.

### Running the Program:
To see Redis Streams in action, you need to run the producer and consumer in separate processes or terminals.

1. **Start the Consumer**:
   Open a terminal and run the consumer script:
   ```bash
   python consumer.py
   ```
   The consumer will start listening for new messages on the `mystream` stream.

2. **Start the Producer**:
   Open another terminal and run the producer script:
   ```bash
   python producer.py
   ```
   The producer will start adding messages to the stream, and the consumer will pick them up and process them.

### Example Output:

**Consumer Terminal**:
```
Listening to the stream: mystream
Received message: {b'user': b'alice', b'message': b'Hello, world!'}
Message ID: 1684116720959-0
Received message: {b'user': b'bob', b'message': b'Hi, everyone!'}
Message ID: 1684116720960-0
Received message: {b'user': b'carol', b'message': b'How\'s it going?'}
Message ID: 1684116720961-0
Received message: {b'user': b'dave', b'message': b'Goodbye!'}
Message ID: 1684116720962-0
```

**Producer Terminal**:
```
Adding message to stream: {'user': 'alice', 'message': 'Hello, world!'}
Adding message to stream: {'user': 'bob', 'message': 'Hi, everyone!'}
Adding message to stream: {'user': 'carol', 'message': 'How\'s it going?'}
Adding message to stream: {'user': 'dave', 'message': 'Goodbye!'}
```

### Explanation:
- **Producer**: The producer generates messages (with `user` and `message` fields) and adds them to the stream `mystream` using `xadd()`.
- **Consumer**: The consumer listens to the stream using `xread()`. It processes each message in the order they are added and prints the message content.

### Key Features of Redis Streams:
1. **Message IDs**: Each message in a Redis stream has a unique ID, which makes it easier to track and manage the messages.
2. **Consumers**: Multiple consumers can read from the same stream. Each consumer can start from a different point in the stream using the message IDs.
3. **Persistence**: Unlike Pub/Sub, Redis Streams provide persistence. Messages are stored in the Redis database until they are acknowledged or deleted.
4. **Consumer Groups**: You can create consumer groups to share the workload of processing messages from the same stream.







