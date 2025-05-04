from pyspark import SparkContext
import time

# Initialize SparkContext
sc = SparkContext(appName="WordCount")

# Read the local file
text_file = sc.textFile(
    "/Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/12-map-reduce/2-spark/11-0.txt",
    minPartitions=8
)

print(text_file.getNumPartitions())
print(text_file.toDebugString())
print(text_file.count())

# print(text_file.coalesce(1).collect())
# <bound method RDD.coalesce of /Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/12-map-reduce/2-spark/11-0.txt MapPartitionsRDD[1] at textFile at NativeMethodAccessorImpl.java:0>

# Perform word count
word_counts = text_file.flatMap(lambda line: line.split()) \
                       .map(lambda word: (word, 1)) \
                       .reduceByKey(lambda a, b: a + b)

print(word_counts.toDebugString())
'''
b'(8) PythonRDD[7] at RDD at PythonRDD.scala:53 []\n 
    |  MapPartitionsRDD[6] at mapPartitions at PythonRDD.scala:160 []\n 
    |  ShuffledRDD[5] at partitionBy at NativeMethodAccessorImpl.java:0 []\n 
    +-(8) PairwiseRDD[4] at reduceByKey at /Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/12-map-reduce/2-spark/wordcount-spark.py:25 []\n    
    |  PythonRDD[3] at reduceByKey at /Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/12-map-reduce/2-spark/wordcount-spark.py:25 []\n    
    |  /Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/12-map-reduce/2-spark/11-0.txt MapPartitionsRDD[1] at textFile at NativeMethodAccessorImpl.java:0 []\n    
    |  /Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/12-map-reduce/2-spark/11-0.txt HadoopRDD[0] at textFile at NativeMethodAccessorImpl.java:0 []'

This output is the result of calling `toDebugString()` on an RDD in your PySpark word count program. Let’s break it down to understand what each part means.

---

### 🧠 **What you’re seeing**

You’re seeing a **lineage DAG (Directed Acyclic Graph)** — a textual representation of **how the final RDD was built** from the original data. Here's a cleaned-up version for clarity:

```
(8) PythonRDD[7] at RDD at PythonRDD.scala:53 []
 |  MapPartitionsRDD[6] at mapPartitions at PythonRDD.scala:160 []
 |  ShuffledRDD[5] at partitionBy at NativeMethodAccessorImpl.java:0 []
 +-(8) PairwiseRDD[4] at reduceByKey at wordcount-spark.py:25 []
    |  PythonRDD[3] at reduceByKey at wordcount-spark.py:25 []
    |  /path/to/11-0.txt MapPartitionsRDD[1] at textFile at NativeMethodAccessorImpl.java:0 []
    |  /path/to/11-0.txt HadoopRDD[0] at textFile at NativeMethodAccessorImpl.java:0 []
```

---

### 🔍 **What each line represents**

* **HadoopRDD\[0]**: Raw input from HDFS or a local file. This is the *starting point*.
* **MapPartitionsRDD\[1]**: Created by `sc.textFile(...)`. This reads and splits the file into lines.
* **PythonRDD\[3]**: Created by your transformation (e.g., `flatMap(lambda line: line.split())`).
* **PairwiseRDD\[4]**: Created by a `map()` that converts words to key-value pairs like `(word, 1)`.
* **ShuffledRDD\[5]**: Created during `reduceByKey`, which involves a shuffle (grouping data by key across partitions).
* **MapPartitionsRDD\[6]**: Spark will apply the reducer logic to each partition.
* **PythonRDD\[7]**: The final RDD you called an action on (like `collect()` or `saveAsTextFile()`).

---

### 📦 Why the `b'...'`?

The `b` prefix means this is a **byte string**. This often happens when printing values returned from subprocesses or when running Spark via scripts. You can convert it to a normal string using:

```python
print(debug_string.decode("utf-8"))
```

---

### ✅ Summary:

* This output shows how Spark builds the final RDD step-by-step from the input file.
* It helps debug performance and understand whether there are expensive operations like shuffles.
* You can trace each transformation by the RDD ID and file/line number (e.g., `wordcount-spark.py:25`).

'''

#
# # Generate a unique output directory name based on the current timestamp
# output_dir = "/Users/mallika/Documents/Anirudh/python/PythonProject/SystemDesign/0-basics/12-map-reduce/2-spark/wordcount_output_" + str(int(time.time()))
#
# # Save the output to a new directory
# word_counts.saveAsTextFile(output_dir)