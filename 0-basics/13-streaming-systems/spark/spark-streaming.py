from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Initialize SparkContext and StreamingContext
sc = SparkContext("local[2]", "WordCountStreaming")  # 2 threads locally
ssc = StreamingContext(sc, 5)  # 1 second batch interval

# Directory where new files are being added continuously (simulating streaming input)
input_dir = "/Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/13-streaming-systems/spark/streaming_data"

# Create DStream from the directory (monitor for new files added every second)
lines = ssc.textFileStream(input_dir)

# Perform word count operations
words = lines.flatMap(lambda line: line.split(" "))  # Split each line into words
word_pairs = words.map(lambda word: (word, 1))  # Create pairs (word, 1)
word_counts = word_pairs.reduceByKey(lambda a, b: a + b)  # Count word occurrences

# Print the word counts
word_counts.pprint()

# Start streaming
ssc.start()

# Await termination of the streaming process
ssc.awaitTermination()
