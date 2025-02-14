import redis

class WriteThroughCache:
    def __init__(self, redis_host, redis_port, redis_db, redis_password=None):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,  # Add password if needed
            decode_responses=True # Important: Decode responses from Redis
        )

    def get(self, key, data_source_function):
        """
        Retrieves a value from the cache. If the value is not in the cache,
        it fetches it using the provided data_source_function, updates the
        cache (write-through), and returns the value.
        """
        try:
            cached_value = self.redis_client.get(key)
            if cached_value:
                return cached_value  # Return from cache if found

            # Cache miss: Fetch from data source
            value = data_source_function(key)  # Execute the function to fetch the value

            if value is not None: # Check if the function returns None
                self.redis_client.set(key, value)  # Write to cache (write-through)
                return value
            else:
                return None # Return None if data source has no value

        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            # Handle the connection error appropriately. For example:
            # 1. Re-raise the exception: raise
            # 2. Return a default value: return None
            # 3. Fallback to another mechanism, etc.
            return None # I'm returning None here as a fallback

    def set(self, key, value):
        """
        Updates the value in the cache and the underlying data source.
        """
        try:
            self.redis_client.set(key, value)  # Update cache
            # In a true write-through cache, you would also update the
            # underlying data source here.  I'm leaving that as a
            # placeholder because the specific update mechanism depends
            # entirely on your data source (database, API, etc.).
            self._update_data_source(key, value)  # Placeholder - Implement this!
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            return None # or raise the exception

    def _update_data_source(self, key, value):
        """
        Placeholder function to update the underlying data source.
        You *must* implement this based on your specific data source.
        """
        # Example for a database (replace with your actual database code):
        # try:
        #     with database_connection() as cursor:
        #         cursor.execute("UPDATE my_table SET value = %s WHERE key = %s", (value, key))
        #         connection.commit()
        # except Exception as e:
        #     print(f"Error updating database: {e}")
        #     raise  # Or handle the error as needed
        raise NotImplementedError("You must implement _update_data_source()")

    def delete(self, key):
        """
        Deletes a key from the cache and the underlying data source.
        """
        try:
            self.redis_client.delete(key)
            self._delete_from_data_source(key) # Placeholder - Implement this!
        except redis.exceptions.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            return None # or raise the exception

    def _delete_from_data_source(self, key):
        """
        Placeholder function to delete from the underlying data source.
        You *must* implement this based on your specific data source.
        """
        raise NotImplementedError("You must implement _delete_from_data_source()")


# Example usage (replace with your Redis connection details and data source logic):
redis_host = "localhost"  # Replace with your Redis host
redis_port = 6379       # Replace with your Redis port
redis_db = 0           # Replace with your Redis database number
redis_password = None # Replace with your Redis password if any

cache = WriteThroughCache(redis_host, redis_port, redis_db, redis_password)

def my_data_source(key):
    # Simulate fetching data from a database or other source
    print(f"Fetching data for {key} from data source...")
    # Replace this with your actual data source logic
    if key == "my_key":
        return "my_value"
    elif key == "another_key":
        return "another_value"
    else:
        return None

value = cache.get("my_key", my_data_source)
print(f"Value: {value}")  # Output: Value: my_value

value = cache.get("my_key", my_data_source) # Retrieve from cache
print(f"Value: {value}")  # Output: Value: my_value (cached)

cache.set("my_key", "my_new_value") # Write through
value = cache.get("my_key", my_data_source) # Retrieve from cache
print(f"Value: {value}")  # Output: Value: my_new_value (updated)

cache.delete("my_key")
value = cache.get("my_key", my_data_source) # Retrieve from cache
print(f"Value: {value}")  # Output: Value: None (deleted)

value = cache.get("non_existent_key", my_data_source)
print(f"Value: {value}")  # Output: Value: None (not found)