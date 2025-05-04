# Spark streaming demo

Execute: spark-streaming.py and write_files_to_dir.py. 

What happens: 
- write_files_to_dir.py

## Basics

1. DStreams (Discretized Streams)    
    - High-level abstraction over streaming data as a series of RDDs.
    - Each batch represents a small window of the live data.
        
2. Micro-Batching Model
    - Processes data in short intervals (e.g., every 1 second).
    - Balances low latency and high throughput.
        
3. In-Memory Processing
    - Keeps intermediate data in memory for fast computation.
    - Ideal for low-latency use cases like real-time analytics and anomaly detection.
        
4. Fault Tolerance
    - Automatically recovers lost data using Spark's lineage model — no complex replication needed.
        
5. Windowed Computations
    - Perform aggregations and analysis over time windows (e.g., last 10 minutes).
        
6. Unified API
    - Same code style for batch and streaming (e.g., `map`, `filter`, `reduceByKey`).
    - Easy transition from batch jobs to streaming pipelines.

📦 Minimal Working Example (File Stream Word Count)

```python
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext("local[2]", "FileStreamWordCount")
ssc = StreamingContext(sc, batchDuration=1)  # 1-second micro-batch

lines = ssc.textFileStream("/path/to/input_dir")
words = lines.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda word: (word, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)

counts.pprint()

ssc.start()
ssc.awaitTermination()
```

⚡ Benefits
- Real-time insights: Spot trends, anomalies, and patterns as they occur.
- Developer productivity: Minimal code change to shift from batch to streaming.
- Scalable and resilient: Handles large-scale streams with ease and recovers from failures automatically.