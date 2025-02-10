from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.common.typeinfo import Types
from pyflink.common.time import Time
from pyflink.common.watermark_strategy import WatermarkStrategy, TimestampAssigner
from pyflink.datastream.functions import MapFunction, ReduceFunction
from datetime import datetime, timedelta
import random

# Sample data simulating ad click events (Ad ID, Click Time)
sample_data = [
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_1", "2025-02-09 12:00:05"),
    ("ad_2", "2025-02-09 12:00:10"),
    ("ad_1", "2025-02-09 12:01:15"),
    ("ad_3", "2025-02-09 12:01:25"),
    ("ad_2", "2025-02-09 12:01:45"),
    ("ad_3", "2025-02-09 12:01:50")
]

def generate_random_datetime(base_datetime_str):
    base_datetime = datetime.strptime(base_datetime_str, "%Y-%m-%d %H:%M:%S")
    random_minutes = random.randint(1, 59)  # Minutes between 1 and 59 (inclusive)
    random_seconds = random.randint(1, 59)  # Seconds between 1 and 59 (inclusive)

    new_datetime = base_datetime + timedelta(minutes=random_minutes, seconds=random_seconds)

    return new_datetime.strftime("%Y-%m-%d %H:%M:%S")


for i in range(1_000_000):
    sample_data.append(
        (f"ad_{random.randint(1, 3)}", generate_random_datetime("2025-02-09 12:00:00"))
    )

# Setup Flink streaming environment
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(20)
env.set_stream_time_characteristic(TimeCharacteristic.EventTime)

# Create a DataStream from the sample data
source = env.from_collection(
    sample_data,
    type_info=Types.TUPLE([Types.STRING(), Types.STRING()])
)

# Function to parse and assign timestamps
class MapWithTimestamps(MapFunction):
    def map(self, value):
        ad_id, timestamp_str = value
        timestamp = int(datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
        return ad_id, timestamp

# Apply the transformation
mapped_stream = source.map(MapWithTimestamps(), output_type=Types.TUPLE([Types.STRING(), Types.LONG()]))

# Define a custom TimestampAssigner
class EventTimeTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp):
        return value[1]  # Use the second element of the tuple as the event timestamp

# Assign timestamps and watermarks
watermarked_stream = mapped_stream.assign_timestamps_and_watermarks(
    WatermarkStrategy.for_monotonous_timestamps().with_timestamp_assigner(EventTimeTimestampAssigner())
)

# Group by Ad ID and apply tumbling window of 1 minute
class CountReducer(ReduceFunction):
    def reduce(self, a, b):
        # a and b are tuples of (ad_id, count)
        # For the first element in the window, the count is initialized to 1
        if isinstance(a, tuple) and isinstance(b, tuple):
            return (a[0], a[1] + 1)  # Increment the count
        elif isinstance(a, tuple):
            return (a[0], 1)  # Initialize count for the first element
        elif isinstance(b, tuple):
            return (b[0], 1)  # Initialize count for the first element
        else:
            return (a[0], 1)  # Fallback

# Apply the windowed aggregation
result_stream = (
    watermarked_stream
    .map(lambda value: (value[0], 1), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))  # Map to (ad_id, 1)
    .key_by(lambda value: value[0])  # Key by ad_id
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))  # 1-minute tumbling window
    .reduce(lambda a, b: (a[0], a[1] + b[1]))  # Reduce to count clicks per ad
)

# Print the result
result_stream.print()

# Execute the Flink job
env.execute("Ad Click Aggregator")
