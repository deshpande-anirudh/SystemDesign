from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, count

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Ad Click Fraud Detection") \
    .getOrCreate()

# Schema for input data
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

schema = StructType([
    StructField("ad_id", StringType(), True),
    StructField("click_time", TimestampType(), True),
    StructField("user_id", StringType(), True)
])

input_directory = "input"

# Read streaming data
df = spark.readStream.schema(schema).csv(input_directory)

# Use watermark for event-time processing to handle late events
click_counts = df.withWatermark("click_time", "1 minute") \
    .groupBy(
        col("user_id"),
        window(col("click_time"), "1 minute")
    ).agg(count("ad_id").alias("click_count"))

# Threshold for fraudulent users
threshold = 10000
fraudulent_users = click_counts.filter(col("click_count") > threshold)

# Write output to the console
query = fraudulent_users.writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()
