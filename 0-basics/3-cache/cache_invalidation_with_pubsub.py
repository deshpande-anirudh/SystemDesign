import redis
import threading
import time

# Redis connection
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Local cache (in-memory)
local_cache = {}

# ====== Writing Data & Publishing Invalidation ======
def update_data(key, value):
    """Update data, invalidate cache, and notify other API instances."""
    print(f"Updating DB: {key} -> {value}")

    # Simulate writing to DB
    time.sleep(1)

    # Update Redis (distributed cache)
    redis_client.set(key, value)

    # Invalidate local cache
    local_cache.pop(key, None)

    # Publish cache invalidation event
    redis_client.publish("cache_invalidation", key)
    print(f"Published invalidation event for: {key}")

# ====== Listening for Cache Invalidation ======
def listen_for_invalidation():
    """Subscribe to cache invalidation events and remove stale local cache keys."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe("cache_invalidation")

    print("Listening for cache invalidation events...")

    for message in pubsub.listen():
        if message["type"] == "message":
            key = message["data"]
            print(f"Invalidating local cache for key: {key}")
            local_cache.pop(key, None)

# Start the invalidation listener in a separate thread
thread = threading.Thread(target=listen_for_invalidation, daemon=True)
thread.start()

# ====== Reading Data with Caching ======
def get_data(key):
    """Retrieve data with local + distributed caching."""
    # Check local cache first
    if key in local_cache:
        print(f"Local cache hit: {key} -> {local_cache[key]}")
        return local_cache[key]

    print(f"Local cache miss: {key}. Fetching from Redis...")

    # Check Redis
    value = redis_client.get(key)
    if value:
        print(f"Redis cache hit: {key} -> {value}")
        local_cache[key] = value  # Store in local cache
        return value

    # If not found in Redis, fetch from DB (simulate)
    value = fetch_from_db(key)
    if value:
        redis_client.set(key, value)  # Update distributed cache
        local_cache[key] = value      # Update local cache
    return value

def fetch_from_db(key):
    """Simulated database fetch"""
    print(f"Fetching {key} from DB...")
    db_data = {"user:1": "Alice", "user:2": "Bob"}  # Example data
    return db_data.get(key)

# ====== Test the PoC ======
if __name__ == "__main__":
    # Simulate data updates
    update_data("user:1", "Alice Updated")

    # Simulate fetching data
    print("\nClient 1 requesting user:1...")
    print(f"Result: {get_data('user:1')}")  # Should fetch from Redis

    print("\nClient 2 requesting user:1...")
    print(f"Result: {get_data('user:1')}")  # Should hit local cache

    # Simulate another update
    print("\nUpdating user:1 again...")
    update_data("user:1", "Alice v2")

    # After a short wait, request again
    time.sleep(2)
    print("\nClient 3 requesting user:1 (after invalidation)...")
    print(f"Result: {get_data('user:1')}")  # Should fetch updated value

    print("\nClient 4 requesting user:1...")
    print(f"Result: {get_data('user:1')}")  # Should hit local cache with updated value
