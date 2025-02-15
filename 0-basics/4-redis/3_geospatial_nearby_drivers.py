import redis
import random

# Connect to Redis server
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Function to add a driver to the Redis geospatial index
def add_driver(driver_id, lat, lon):
    # Ensure that only the required arguments are passed
    r.geoadd('cars:locations', (lon, lat, driver_id))
    print(f"Driver {driver_id} added at latitude {lat}, longitude {lon}")

# Function to find nearby drivers within a certain radius
def find_nearby_drivers(lat, lon, radius, unit='mi'):
    # Find drivers within the specified radius (default is miles)
    nearby_drivers = r.georadius('cars:locations', lon, lat, radius, unit, withdist=True)
    if nearby_drivers:
        print(f"Nearby drivers within {radius} {unit}:")
        for driver in nearby_drivers:
            driver_id, distance = driver
            print(f"Driver ID: {driver_id}, Distance: {distance} {unit}")
    else:
        print("No nearby drivers found")

# Function to generate random latitude and longitude within a given region (for example, New York)
def generate_random_location():
    # New York latitude and longitude bounds
    lat_min, lat_max = 40.477399, 40.917577
    lon_min, lon_max = -74.259090, -73.700272

    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)
    return lat, lon

# Function to simulate adding 100 drivers at random locations
def add_random_drivers():
    for i in range(1, 101):
        driver_id = f'driver{i}'
        lat, lon = generate_random_location()
        add_driver(driver_id, lat, lon)

# Function to simulate querying nearby drivers from 10 distant locations
def query_from_multiple_locations():
    # Generate 10 random locations to query from
    for i in range(1, 11):
        lat, lon = generate_random_location()
        print(f"\nQuerying from location {i}: Latitude {lat}, Longitude {lon}")
        find_nearby_drivers(lat, lon, 10)  # 10-mile radius

# Example usage
if __name__ == "__main__":
    # Add 100 random drivers
    add_random_drivers()

    # Query from 10 random locations
    query_from_multiple_locations()
