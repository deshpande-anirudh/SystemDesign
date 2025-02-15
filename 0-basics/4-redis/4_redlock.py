import redis
import time
import uuid


class Redlock:
    def __init__(self, redis_clients, lock_key, ttl_ms):
        """
        Initialize Redlock with a list of Redis clients, lock key, and TTL for the lock.

        :param redis_clients: List of Redis client instances.
        :param lock_key: The key to be used for the lock in Redis.
        :param ttl_ms: Time to live for the lock in milliseconds.
        """
        self.redis_clients = redis_clients
        self.lock_key = lock_key
        self.ttl_ms = ttl_ms
        self.quorum = len(redis_clients) // 2 + 1

    def acquire(self):
        """
        Try to acquire the lock from the Redis nodes.

        :return: The lock value (UUID) if acquired successfully, None otherwise.
        """
        lock_value = str(uuid.uuid4())
        start_time = time.time()
        locks_acquired = 0

        # Try to acquire the lock from each Redis node
        for redis_client in self.redis_clients:
            result = redis_client.set(self.lock_key, lock_value, nx=True, px=self.ttl_ms)
            if result:
                locks_acquired += 1

        # Check if we have acquired a majority of locks
        if locks_acquired >= self.quorum:
            # Lock acquired
            return lock_value

        # Release the lock if not acquired on all nodes
        self.release(lock_value)
        return None

    def release(self, lock_value):
        """
        Release the lock on all Redis nodes.

        :param lock_value: The value (UUID) to be checked and released.
        """
        for redis_client in self.redis_clients:
            # Lua script to check if the lock value matches before releasing
            lua_script = """
                if redis.call('get', KEYS[1]) == ARGV[1] then
                    return redis.call('del', KEYS[1])
                else
                    return 0
                end
            """
            redis_client.eval(lua_script, 1, self.lock_key, lock_value)

    def is_locked(self):
        """
        Check if the lock is currently held on any Redis node.

        :return: True if the lock exists, False otherwise.
        """
        for redis_client in self.redis_clients:
            if redis_client.exists(self.lock_key):
                return True
        return False


# Example usage
if __name__ == "__main__":
    # Connect to Redis instances (replace with your actual Redis hosts)
    redis_clients = [
        redis.StrictRedis(host='localhost', port=6379, db=0),
        redis.StrictRedis(host='localhost', port=6380, db=0),
        redis.StrictRedis(host='localhost', port=6381, db=0)
    ]

    lock = Redlock(redis_clients, "my_lock_key", ttl_ms=10000)

    # Try to acquire the lock
    lock_value = lock.acquire()

    if lock_value:
        print(f"Lock acquired with value: {lock_value}")

        # Perform some critical section work
        time.sleep(5)

        # Release the lock after the work is done
        lock.release(lock_value)
        print("Lock released")
    else:
        print("Failed to acquire the lock")
