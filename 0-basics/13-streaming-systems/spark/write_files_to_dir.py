import shutil
import time

# Path to the source file
source_file = "/Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/13-streaming-systems/spark/11-0.txt"

# Path to the directory Spark Streaming will monitor
destination_dir = "/Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/13-streaming-systems/spark/streaming_data"

while True:
    # Copy the file to the directory (this simulates streaming by adding files periodically)
    timestamp = str(int(time.time()))  # Create a unique file name using timestamp
    destination_file = f"{destination_dir}/file_{timestamp}.txt"

    shutil.copy(source_file, destination_file)  # Copy file to the "streaming" directory

    print(f"Added {destination_file}")  # Print confirmation message

    time.sleep(1)