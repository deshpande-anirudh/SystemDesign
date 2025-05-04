from pyspark import SparkContext
import time

sc = SparkContext("local", "RDD Example")

start = time.monotonic()
nums_rdd = sc.parallelize(
    [x for x in range(1, 1_000_000)]
)
print(nums_rdd.getNumPartitions())
result_rdd = (nums_rdd
              .map(lambda num: num + num))

print(result_rdd.collect())
no_slice_seconds = time.monotonic() - start

start = time.monotonic()
nums_rdd = sc.parallelize(
    [x for x in range(1, 1_000_000)],
    50
)
# print(nums_rdd.getNumPartitions())
result_rdd = (nums_rdd
              .map(lambda num: num + num))

# print(result_rdd.collect())
fifty_slice_seconds = time.monotonic() - start

start = time.monotonic()
nums_rdd = sc.parallelize(
    [x for x in range(1, 1_000_000)],
    500
)
print(nums_rdd.getNumPartitions())
result_rdd = (nums_rdd
              .map(lambda num: num + num))

# print(result_rdd.collect())
five_hundred_slice_seconds = time.monotonic() - start

print(f'No slices: took {no_slice_seconds} seconds.')
print(f'Fifty slices: took {fifty_slice_seconds} seconds.')
print(f'Five hundred slices: took {five_hundred_slice_seconds} seconds.')

sc.stop()


'''
No slices: took 1.936790583000402 seconds.
Fifty slices: took 3.1789012499939417 seconds.
Five hundred slices: took 27.21971383401251 seconds.
'''