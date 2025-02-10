from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, count
import os

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Ad Click Aggregation") \
    .getOrCreate()

# Path to the CSV file containing click data
input_directory = "input"
input_file_path = os.path.join(input_directory, "input.csv")


# Load the CSV file into a DataFrame
df = spark.read.csv(input_file_path, header=True, inferSchema=True)

# Assuming the CSV has columns named 'ad_id' and 'click_time'
# Convert 'click_time' column to timestamp
df = df.withColumn("click_time", col("click_time").cast("timestamp"))

# Group by ad ID and 1-minute time window, then count the number of clicks per window
df_grouped = df.groupBy(
    col("ad_id"),
    window(col("click_time"), "1 minute")
).agg(count("click_time").alias("click_count"))

# Flatten the window struct by selecting its start and end components
df_flattened = df_grouped.select(
    col("ad_id"),
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("click_count")
)

# Show the result
df_flattened.show(truncate=False)
print(f"Number of partitions: {df_flattened.rdd.getNumPartitions()}")

# Write the result to an output file (optional)
output_file_path = "output"
df_flattened.write.csv(output_file_path, header=True, mode='overwrite')

print(df.rdd.toDebugString())


# Stop the Spark session
spark.stop()
