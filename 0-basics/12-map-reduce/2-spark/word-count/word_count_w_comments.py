from pyspark import SparkContext
import time

# SparkContext is the entry point for interacting with Spark,
# managing the connection to the cluster, and coordinating the execution of jobs and tasks.
# Can be HDFS etc.
sc = SparkContext("local", "WordCount")

# Reads the text file from the specified path and creates an RDD with a minimum of 4 partitions
# to distribute the file across multiple nodes for parallel processing.
text_file_rdd = sc.textFile(
    "/Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/12-map-reduce/2-spark/word-count/11-0.txt",
    minPartitions=4
)

word_count_rdd = (text_file_rdd
    # Splits each line into words and flattens the result into a single list
    .flatMap(lambda line: line.split(" "))
    # Maps each word to a key-value pair (word, 1)
    .map(lambda word: (word, 1))
    # Reduces the key-value pairs by summing the values for each word
    .reduceByKey(lambda a, b: a + b)
    # Sorts the words by their count in descending order
    .sortBy(lambda x: -x[1])
    )

word_counts = word_count_rdd.collect()
sc.stop()
