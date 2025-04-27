# How the broker stores the messages 

![](https://plantuml.online/png/pL9DJyCm3BtdL_ZO7gYsyN50OjBO5QH97BXm2QcRHctZoGbCuzVZgTsQ8eGcJil5YVoUtxDZRI8nR9ZA3uEiq4SNz_38r8olZMQ9ZlmJMQMEMBXQ3ZYuXnVq9JnZ2DeYPAMEEbT3Kc1f0G6lQpGDh4nqdoXCsucEcc3IqbCSPBFqp6UB6mb5I_OFmTLsc_gBTBRucdpbk3jH-qfAUOe8x6mTWQeHFbmiUcGTCKYo2YYcUv_pNAKcZuCyzDXushLOYiGhEwcT3Sm76AbJqPyzdZicODIc5c_1VI6qhdE2baGHUchnlXVd-PkV21XX7HhIu747uNULs-kxqsTSs9warYv-JnR_tnEXVWC0)

### **Explanation:**
1. **Producer sends a message** to the broker with an offset (`1024001`).
2. The broker **checks the active segment** of the partition log.
3. The broker **appends the message** to the current active segment (`00000000000001024000.log`).
4. Once the message is successfully appended, the broker sends an **acknowledgment** to the producer.
5. After the **active segment reaches the size limit**, Kafka creates a new log segment (`00000000000001536000.log`).
6. When a new message arrives (`1024002`), the broker repeats the process but appends the message to the **new active segment**.

# Detailed explanation

1. Producer Sends the Message: 
   1. The producer sends a message to the leader broker, but the producer doesn't specify the offset. 
   2. It only specifies the message data and, optionally, a key for partitioning.
   3. Since Kafka writes logs **sequentially**, disk I/O is minimal, ensuring high throughput.
2. Broker Appends the Message: 
   1. The leader **writes the message to the log segment** of the partition. 
   2. The message gets an **offset**, ensuring an **ordered, immutable log**.
   3. The write is performed in an **append-only** manner for fast I/O.  .
3. If the topic has **replication enabled** (e.g., RF=3), the leader **sends the message to follower replicas**.  
   1. Followers fetch data via **pull-based replication**.  
   2. The leader waits for acknowledgments from followers **depending on the `acks` setting**:
     - `acks=1`: Leader acknowledges after writing the message.  
     - `acks=all`: Leader waits for all in-sync replicas (ISRs) to confirm replication.  
4. Producer Acknowledgment: Once the message is successfully written to the partition, the broker sends an acknowledgment to the producer, which includes the offset assigned to the message.
   1. Once the write is **successfully committed**, the broker sends an **ACK** back to the producer.  
   2. The producer **removes the message from its retry queue** (if applicable).  
5. The message is now **available for consumers**.  
   1. Consumers fetch data in **offset order** using `poll()`.  
   2.The broker **retains the message** based on retention settings (`log.retention.ms`, `log.retention.bytes`).

-------

# How big is the Kafka partition?

1️⃣ **Log Segment Size (`log.segment.bytes`)**  
   - Default: **1GB** (1,073,741,824 bytes)  
   - When a segment reaches this size, Kafka rolls over to a new log segment file.  

2️⃣ **Retention Settings**  
   - **Time-based (`log.retention.hours`)**: Deletes old segments (default **168 hours / 7 days**)  
   - **Size-based (`log.retention.bytes`)**: Retains only up to a specified storage limit  

3️⃣ **Message Size (`message.max.bytes`)**  
   - Default: **1MB** per message  
   - Can be configured for larger messages  

### **How Log Segments Work**  
- Each **partition** consists of **multiple log segment files**.  
- A segment remains **active** until it reaches `log.segment.bytes`.  
- Once a segment is full, Kafka **creates a new segment** and the old ones remain until **log retention policies** delete them.  

💡 **Example:**  
- Partition log file **grows until** 1GB per segment.  
- If messages are small, many records fit in 1GB.  
- If messages are large (e.g., 10MB each), only ~100 messages fit in a 1GB segment.

--------

# Does one partition contain many segment files?

1️⃣ **Active and Rolled Segments**  
   - Each partition has **one active segment** where new messages are written.  
   - When the active segment reaches the `log.segment.bytes` limit (default **1GB**), Kafka **creates a new segment**.  
   - Older segments remain on disk until **retention policies** clean them up.  

2️⃣ **Log Segment Naming**  
   - Each segment file is named based on the **starting offset** of the first message in that segment.  
   - Example:
     ```
     00000000000000000000.log  # First segment
     00000000000000100000.log  # Second segment (starting at offset 100000)
     00000000000000200000.log  # Third segment (starting at offset 200000)
     ```

3️⃣ **Segment Retention and Deletion**  
   - Kafka **deletes older segments** based on:  
     - **Time (`log.retention.hours`)** → Deletes segments older than a configured duration.  
     - **Size (`log.retention.bytes`)** → Keeps total partition data within a set limit.  
   - Only **fully closed** segments are eligible for deletion—**the active segment is never deleted**.  

### **Example Scenario**
- A topic **"orders"** has **Partition-0** on **Broker-1**.  
- `log.segment.bytes = 512MB`, `log.retention.hours = 168 (7 days)`.  
- Messages keep getting added to **Partition-0**.  
- Once the **current segment** hits 512MB, Kafka **creates a new segment** and continues writing there.  
- **Old segments** get deleted when they **exceed retention limits**.  

### **Conclusion**
✔ **Yes, a topic partition has multiple segments.**  
✔ **Only one active segment per partition** (new writes go here).  
✔ **Old segments remain until retention policy deletes them.**  
 

```
Topic: "orders"
Partition: 0 (Stored on Broker-1)

+--------------------+
|  Active Segment   |  <-- New messages are written here
|  000000000300000.log |
+--------------------+

+--------------------+
|  Log Segment 2    |  
|  000000000200000.log |
+--------------------+

+--------------------+
|  Log Segment 1    |  
|  000000000100000.log |
+--------------------+

+--------------------+
|  Log Segment 0    |  <-- Oldest segment
|  000000000000000.log |
+--------------------+
```

-------------

The **Kafka broker** determines which **log segment** to append a message to based on the **partition's current active log segment**. Each **topic partition** has its own log file segments, and the broker manages these segments through the following process:

### **Log Segment Lifecycle for a Broker**:

1. **Log Segment Structure**:
   - Each partition's log is split into **log segments**, and each segment is a file on disk.
   - A log segment is named after its **starting offset**. For example, `00000000000000000000.log` (where `00000000000000000000` is the first offset in that segment).

2. **Identifying the Active Segment**:
   - Kafka **keeps track of the most recent segment** that is still being written to. This is called the **active segment**.
   - New messages are **always appended** to this active segment.
   - The active segment file remains open for writing until it reaches the configured **segment size limit** (`log.segment.bytes`) or the **time-based segment rollover** limit (`log.roll.ms` or `log.roll.hours`).
  
3. **When to Create a New Segment**:
   - **When the active segment reaches the configured size limit** (e.g., `log.segment.bytes = 1GB`), a new segment is created automatically. The **old segment** becomes **read-only**, and Kafka starts writing to the new segment.
   - **Time-based rollovers** (if configured, e.g., `log.roll.ms = 86400000` for 24 hours) will force a new segment even if the previous segment hasn't reached the size limit.

4. **Storing Data**:
   - When a message comes in from the producer, Kafka **appends the message** to the **active segment**.
   - The broker maintains a **file pointer** or internal tracking mechanism to identify the end of the current segment and the next available position to append data.

### **Flow Example**:
- Suppose you have a topic with a partition, and the `log.segment.bytes` is set to 512MB.
- The partition has three log segments:
  1. `00000000000000000000.log` (started at offset `0`)
  2. `00000000000000512000.log` (started at offset `512000`)
  3. `00000000000001024000.log` (started at offset `1024000`) - **current active segment**.

  When a message with **offset `1024001`** arrives, it will be **appended to the `00000000000001024000.log` segment**.

- Once this segment exceeds the configured size limit (e.g., 512MB), a **new segment** will be created, and the next messages will be written to it.

### **Segment Metadata Management**:
- Kafka **stores metadata about the active segment** and the **range of offsets in each segment**.
- This metadata is critical for efficient message retrieval and managing segments for retention/compaction.

---

### **Summary**:
- The **broker determines which log segment** to append to based on the **current active segment**.
- The active segment is the one being written to, and once full (based on size or time), Kafka **creates a new segment**.
- Each partition's log is divided into multiple segments, and **Kafka ensures efficient writes** by appending to the correct segment.

-----------------
