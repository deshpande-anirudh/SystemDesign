import threading
import time
import functools

cache = {}
cache_locks = {}


def cached_function(key, expensive_operation):
    """
    Decorator for caching with thundering herd prevention.
    """
    @functools.wraps(expensive_operation)  # Preserve original function metadata
    def wrapper(*args, **kwargs):
        global cache, cache_locks  # Access outer scope variables

        # 1. Check if the key is already in the cache
        if key in cache:
            return cache[key]

        # 2. Check if a lock exists for this key. Create one if it does not
        if key not in cache_locks:
            cache_locks[key] = threading.Lock()

        lock = cache_locks[key]

        with lock:  # Only one thread can enter this block at a time for a given key
            # 3. Double-check if the value is now in the cache (another thread
            #    might have populated it while we were waiting for the lock)
            if key in cache:
                return cache[key]

            # 4. If not in the cache, perform the expensive operation
            result = expensive_operation(*args, **kwargs)

            # 5. Store the result in the cache
            cache[key] = result

            # 6. (Optional) Remove the lock if you don't expect repeated updates
            #    for the key. This prevents lock accumulation.
            # del cache_locks[key]  # Careful with this! See explanation below

            return result

    return wrapper


# Example expensive operation (simulating a database call or complex computation)
def _expensive_calculation(x):
    print(f"Calculating for {x}...") # Show that the calculation is only done once
    time.sleep(2)  # Simulate some work
    return x * 2


# Make the expensive function cached
expensive_calculation = cached_function("my_key", _expensive_calculation) # Cache with key "my_key"

# Simulate multiple concurrent requests for the same key
threads = []
for _ in range(5):
    t = threading.Thread(target=lambda: print(expensive_calculation(5))) # Pass any value here
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(cache) # Print the final cache

# Example with different keys
expensive_calculation_2 = cached_function("my_key_2", _expensive_calculation)
print(expensive_calculation_2(10))
print(cache)
