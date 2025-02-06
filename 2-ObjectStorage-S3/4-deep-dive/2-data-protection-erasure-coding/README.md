# Erasure Coding Demo with Reed-Solomon in Python

This project demonstrates the use of Reed-Solomon erasure coding to protect and recover data in distributed storage systems. The code encodes a sample message with parity symbols, simulates data corruption, and attempts to recover the original data.

## What is Erasure Coding?
Erasure coding is a data protection technique used in distributed systems to ensure data durability and availability. It involves breaking data into smaller chunks, encoding it with additional parity chunks, and distributing both data and parity across storage nodes.

### Key Benefits
- **Fault Tolerance:** Allows data recovery even when multiple nodes or drives fail.
- **Storage Efficiency:** Requires less storage overhead compared to simple replication methods.
- **Scalability:** Suitable for large-scale distributed systems.

### How It Works
In a typical erasure coding scheme, data is split into `k` data chunks and `m` parity chunks, often written as `(k, m)`. The total chunks `n = k + m` are stored across different locations. Even if up to `m` chunks are lost, the original data can still be reconstructed.

Example: In a `(4, 2)` erasure coding setup, four data blocks and two parity blocks are created. The system can tolerate the loss of any two blocks.

### What is Parity?
Parity is a form of error detection and correction information generated alongside data. In the context of erasure coding, parity blocks store additional information derived from the data blocks, enabling the reconstruction of original data even when some parts are lost or corrupted.

In simple terms, parity allows the system to "fill in the blanks" if some data becomes inaccessible, much like solving a puzzle using the remaining pieces and clues.

## How It Works in This Demo
1. **Encoding:** The data is encoded with parity symbols for error correction.
2. **Data Corruption:** A portion of the encoded data is deliberately corrupted by flipping random bits.
3. **Data Recovery:** The system attempts to recover the original data using Reed-Solomon error correction.

## Requirements
- Python 3.x
- `reedsolo` library for Reed-Solomon error correction

### Installation
```bash
pip install reedsolo
```

## Usage
1. Run the script to see how data is encoded, corrupted, and recovered.
2. Modify the `data` variable to test with different data strings.

### Example Output
```
Original Data: b'Hello, this is a demo of erasure coding!'
Encoded Data: bytearray(b'Hello, this is a demo of erasure coding!...')
Corrupted Data: bytearray(b'Hello, this is a demo of erasure...')
Recovered Data: b'Hello, this is a demo of erasure coding!'
```

## Code Overview
### Encoding
The following line encodes the data with 20 parity symbols:
```python
encoded_data = rs.encode(data)
```
### Data Corruption
To simulate corruption, the code flips random bits at five positions:
```python
corrupted_data = bytearray(encoded_data)
for _ in range(5):
    idx = random.randint(0, len(corrupted_data) - 1)
    corrupted_data[idx] ^= 0xFF  # Flip some bits to corrupt
```
### Recovery
The Reed-Solomon decoder attempts to recover the original data:
```python
recovered_data = rs.decode(corrupted_data)
```

## Error Handling
If too much data is corrupted, the following error may occur:
```
ReedSolomonError: Too many (or few) errors found by Chien Search
```
To avoid this, ensure that the number of corrupted bytes does not exceed half the parity symbols.

## Suggested Improvements
- Experiment with different levels of corruption and parity symbols.
- Handle exceptions gracefully to provide user-friendly error messages.

## License
This project is open-source and available under the MIT License.
