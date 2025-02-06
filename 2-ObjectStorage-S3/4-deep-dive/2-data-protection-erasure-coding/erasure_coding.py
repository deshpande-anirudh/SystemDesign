import reedsolo
import random

# Initialize the Reed-Solomon encoder
rs = reedsolo.RSCodec(20)  # 10 parity symbols for error correction

# Example data to encode
data = b"Hello, this is a demo of erasure coding!"
print(f"Original Data: {data}")

# Encode the data with parity
encoded_data = rs.encode(data)
print(f"Encoded Data: {encoded_data}")

# Simulate data corruption (remove 10 bytes)
# Corrupt 5 bytes randomly
corrupted_data = bytearray(encoded_data)
for _ in range(5):
    idx = random.randint(0, len(corrupted_data) - 1)
    corrupted_data[idx] ^= 0xFF  # Flip some bits to corrupt
print(f"Corrupted Data: {corrupted_data}")

try:
    # Attempt to decode and recover the data
    recovered_data = rs.decode(corrupted_data)
    print(f"Recovered Data: {recovered_data}")
except reedsolo.ReedSolomonError as e:
    print("Failed to recover data:", e)
