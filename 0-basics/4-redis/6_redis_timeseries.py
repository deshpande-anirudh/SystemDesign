import redis
import random
import time
from datetime import datetime, timedelta

# Connect to Redis server with RedisTimeSeries enabled
r = redis.StrictRedis(host='localhost', port=6379, db=0)


# Add temperature readings to a sensor's timeseries
def add_temperature_reading(sensor_id, timestamp, temperature):
    # Create a unique timeseries key for each sensor
    ts_key = f"sensor:{sensor_id}:temperature"

    # Add the temperature reading to the timeseries
    r.ts().add(ts_key, timestamp, temperature)
    print(f"Added temperature {temperature}°C at {timestamp} for sensor {sensor_id}")


# Query temperature data within a specific time range
def query_temperature(sensor_id, start_time, end_time):
    ts_key = f"sensor:{sensor_id}:temperature"

    # Use the TS.RANGE command to get the data within the specified range
    readings = r.ts().range(ts_key, start_time, end_time)

    if readings:
        print(f"\nTemperature readings for sensor {sensor_id} between {start_time} and {end_time}:")
        for timestamp, temperature in readings:
            timestamp = datetime.utcfromtimestamp(timestamp / 1000)  # Convert timestamp to datetime
            print(f"Time: {timestamp}, Temperature: {temperature}°C")
    else:
        print(f"No readings found for sensor {sensor_id} in the given time range.")


# Simulate adding random temperature data for multiple sensors
def add_random_temperature_data():
    for sensor_id in range(1, 6):  # Simulate 5 sensors
        for _ in range(10):  # Each sensor adds 10 readings
            # Generate a random temperature reading between -10°C and 40°C
            temperature = random.uniform(-10, 40)
            # Generate a random timestamp within the last 24 hours
            timestamp = int((datetime.now() - timedelta(days=random.randint(0, 1))).timestamp() * 1000)
            add_temperature_reading(sensor_id, timestamp, temperature)
            time.sleep(1)  # Simulate time delay between readings


# Example usage
if __name__ == "__main__":
    # Add random temperature data for 5 sensors
    add_random_temperature_data()

    # Query temperature readings for sensor 1 in the last hour
    start_time = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    query_temperature(sensor_id=1, start_time=start_time, end_time=end_time)
