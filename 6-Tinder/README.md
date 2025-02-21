# Race conditions

If two users swipe right on each other *instantaneously* in a distributed system like Tinder, the main consistency issues that could arise include:

### 1. **Race Conditions**
   - If both users swipe at almost the exact same time, separate servers (or database nodes) handling their requests may not see the other's swipe immediately.
   - This could lead to scenarios where both users believe they haven't matched yet, even though the system will eventually reconcile the match.

### 2. **Duplicate Matches**
   - If there’s no proper deduplication, both users could receive two match notifications instead of one.
   - This might happen if each user’s swipe creates an independent entry in the database, which isn't deduplicated correctly.

### 3. **Eventual Consistency Delays**
   - If a system like Tinder uses **eventual consistency** (e.g., with an eventually consistent NoSQL database like DynamoDB), one user might see the match immediately while the other doesn't until replication completes.
   - This can lead to confusion where one user can send a message while the other still sees the match as pending.

### 4. **Concurrency Control Issues**
   - If multiple replicas or microservices handle different users' swipe actions, they might not have a synchronized view of the swipes.
   - Without proper concurrency control (e.g., optimistic locking, transactions, or idempotent operations), there might be cases where:
     - The system incorrectly processes only one swipe, leading to an incomplete match.
     - A retry mechanism could reprocess a swipe multiple times.

### 5. **Ordering Issues**
   - In a distributed setup, one swipe could be recorded before the other, leading to different states appearing in different places.
   - For example, User A sees “Matched” instantly, but User B still sees a pending swipe due to network or database delays.

### 6. **Network Partitioning**
   - If a network partition happens, one user might swipe, but the other user’s swipe isn't processed immediately.
   - Once the network is restored, the system has to reconcile these delayed swipes, potentially leading to stale state updates.

### **Solution Approaches**
- **Atomic Match Creation**: Use a transaction-like mechanism to ensure both swipes result in a single match entry.
- **Deduplication Logic**: Ensure match creation is idempotent.
- **Consistency Model Choice**: If using eventual consistency, add retries or real-time notifications to inform users of match updates.
- **Vector Clocks or Timestamps**: Track swipe events and resolve conflicts based on timestamps.

# Atomic operations with REDIS and Lua script

To achieve **atomic match creation** in Redis, we can use Redis transactions (`MULTI`/`EXEC`) or **Lua scripting**, which ensures atomicity. The idea is:

1. When a user swipes right, store their swipe in a Redis **set**.
2. Before storing, check if the other user has already swiped right.
3. If both users have swiped right, create a **match entry** atomically.

Here’s how you can do it using **Redis Lua scripting** to ensure atomicity:

### **Redis Schema**
- `swipes:{user_id}` → A Redis **set** storing users this user has swiped right on.
- `matches:{user1}:{user2}` → A Redis **key** indicating a match.

---

### **Atomic Match Creation with Redis Lua Script**
```python
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

MATCH_SCRIPT = """
local user1 = KEYS[1]
local user2 = KEYS[2]
local matchKey = KEYS[3]

-- Check if user2 has already swiped on user1
if redis.call('SISMEMBER', user2, user1) == 1 then
    -- Create a match atomically
    redis.call('SET', matchKey, 'matched')
    return 'matched'
else
    -- Otherwise, store the swipe
    redis.call('SADD', user1, user2)
    return 'pending'
end
"""

def swipe_right(user1, user2):
    """
    User1 swipes right on User2. If User2 has already swiped on User1, a match is created.
    """
    match_key = f"matches:{min(user1, user2)}:{max(user1, user2)}"
    swipe_key_user1 = f"swipes:{user1}"
    swipe_key_user2 = f"swipes:{user2}"

    result = r.eval(MATCH_SCRIPT, 3, swipe_key_user1, swipe_key_user2, match_key)
    return result

# Example Usage
print(swipe_right("alice", "bob"))  # First swipe → "pending"
print(swipe_right("bob", "alice"))  # Second swipe → "matched"
```

---

### **How It Works**
1. When **Alice swipes right on Bob**, we:
   - Check if Bob already swiped right on Alice.
   - If not, add Alice's swipe (`SADD swipes:alice bob`).
   - Return `"pending"`.
   
2. When **Bob swipes right on Alice**, we:
   - Check if Alice already swiped.
   - If yes, **create a match** (`SET matches:alice:bob matched`).
   - Return `"matched"`.

### **Why This is Atomic?**
- **Lua scripts in Redis are atomic**: The script runs in a single Redis command execution, preventing race conditions.
- **No race condition**: Even if Alice and Bob swipe at exactly the same time, the check and update operations are performed atomically.

# Pubsub notifications on a match

To notify users in real-time when a match occurs, we can use **Redis Pub/Sub**. Here's how:  

1. When a match is created, publish a message to a Redis **Pub/Sub channel** (`matches_channel`).
2. Clients (e.g., WebSocket server, push notification service) subscribe to this channel to receive match events.
3. When a user swipes, if a match is detected, publish a message notifying both users.

---

### **Updated Code with Pub/Sub Notification**
```python
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

MATCH_SCRIPT = """
local user1 = KEYS[1]
local user2 = KEYS[2]
local matchKey = KEYS[3]
local channel = KEYS[4]

-- Check if user2 has already swiped on user1
if redis.call('SISMEMBER', user2, user1) == 1 then
    -- Create a match atomically
    redis.call('SET', matchKey, 'matched')
    
    -- Publish match event
    redis.call('PUBLISH', channel, user1 .. ":" .. user2)
    
    return 'matched'
else
    -- Otherwise, store the swipe
    redis.call('SADD', user1, user2)
    return 'pending'
end
"""

def swipe_right(user1, user2):
    """
    User1 swipes right on User2. If User2 has already swiped on User1, a match is created and a notification is published.
    """
    match_key = f"matches:{min(user1, user2)}:{max(user1, user2)}"
    swipe_key_user1 = f"swipes:{user1}"
    swipe_key_user2 = f"swipes:{user2}"
    channel = "matches_channel"

    result = r.eval(MATCH_SCRIPT, 4, swipe_key_user1, swipe_key_user2, match_key, channel)
    return result

# Example Usage
print(swipe_right("alice", "bob"))  # First swipe → "pending"
print(swipe_right("bob", "alice"))  # Second swipe → "matched" + Notification Published
```

---

### **Listening for Match Events (Subscriber)**
A service (e.g., a WebSocket server or push notification service) subscribes to `matches_channel` and listens for match notifications.

```python
def listen_for_matches():
    pubsub = r.pubsub()
    pubsub.subscribe("matches_channel")
    
    print("Listening for matches...")
    for message in pubsub.listen():
        if message["type"] == "message":
            user1, user2 = message["data"].split(":")
            print(f"🔥 Match Alert! {user1} and {user2} have matched!")

# Start listening
listen_for_matches()
```

---

### **How It Works**
1. When **Alice swipes right on Bob**, it gets stored as a pending swipe.
2. When **Bob swipes right on Alice**, a **match is created**:
   - A key (`matches:alice:bob`) is set.
   - A **match event is published** on `matches_channel`.
3. The **subscriber** (push notification service or WebSocket) listens for the event and notifies users.

---

### **Next Steps**
- Integrate this with a WebSocket server to **push match notifications in real time**.
- Use a **message queue (e.g., Kafka, SQS)** for better scalability.
- Trigger **push notifications** via Firebase or Apple Push Notification Service (APNS).

# Real-time notifications with web-sockets

To integrate **real-time notifications** using **WebSockets**, we’ll do the following:  

1. **Redis handles the match logic and publishes events.**  
2. **A WebSocket server subscribes to Redis Pub/Sub (`matches_channel`).**  
3. **When a match occurs, the WebSocket server sends a message to connected clients.**  

---

## **Setup WebSocket Server (FastAPI + WebSockets)**
We'll use **FastAPI** to handle WebSocket connections and Redis for pub/sub.

### **Install Dependencies**
```sh
pip install fastapi uvicorn redis
```

---

### **WebSocket Server with Redis Subscription**
```python
import redis
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

app = FastAPI()

# Redis connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Store active WebSocket connections
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    Handles WebSocket connections for users.
    """
    await websocket.accept()
    active_connections[user_id] = websocket
    print(f"User {user_id} connected")

    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        del active_connections[user_id]
        print(f"User {user_id} disconnected")


async def listen_for_matches():
    """
    Listens for match events from Redis and sends real-time notifications via WebSockets.
    """
    pubsub = r.pubsub()
    pubsub.subscribe("matches_channel")

    print("Listening for match events...")
    for message in pubsub.listen():
        if message["type"] == "message":
            user1, user2 = message["data"].split(":")

            # Notify users if they are connected
            if user1 in active_connections:
                await active_connections[user1].send_text(f"🔥 You matched with {user2}!")
            if user2 in active_connections:
                await active_connections[user2].send_text(f"🔥 You matched with {user1}!")


# Start listening for matches in the background
@app.on_event("startup")
async def start_listener():
    asyncio.create_task(listen_for_matches())

```

---

## **How It Works**
1. **Users connect to `/ws/{user_id}` via WebSocket.**  
   - Their WebSocket is stored in `active_connections`.  
2. **When a match occurs (`swipe_right()` from previous implementation)**  
   - Redis publishes a message: `"alice:bob"`.  
3. **The WebSocket server listens for this event**  
   - If Alice or Bob is connected, they receive a **real-time notification** via WebSockets.  

---

### **Running the Server**
```sh
uvicorn filename:app --host 0.0.0.0 --port 8000
```

---

### **Testing WebSockets**
1. Open two browser tabs (or use `wscat` CLI)  
2. Connect WebSockets:
   ```sh
   wscat -c ws://localhost:8000/ws/alice
   wscat -c ws://localhost:8000/ws/bob
   ```
3. Trigger a **match event** (by running `swipe_right("alice", "bob")` from the previous script).  
4. Both Alice and Bob should receive **🔥 "You matched with [other user]!"**  

---

## **Next Steps**
- **Integrate WebSockets with a frontend** (React, Vue, etc.).
- **Use Redis Cluster for scalability.**
- **Extend this to send push notifications (Firebase/APNS).**
