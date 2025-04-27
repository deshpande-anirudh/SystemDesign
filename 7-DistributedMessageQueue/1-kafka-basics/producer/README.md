# Kafka Producer

![](https://plantuml.online/png/hLFHYjim47pNLoptv413wUk1Myv7GqkSSYGKsiSzQPq8Av8hoPUxl-_Qibqxrr8ApOk3DJCxgncZZCx3WtUgbUH5WpvggHkq4Mvs555XHBX7UIB8FjlrZixElwnk04DwksGKpiKGFJPm8Fz4liSLXoMe95JaeV2kvaVsq9r5xInyIxfbiSHld37kCZ42P7jgZ9ROaH9bSqNPObKZbEx8yipG8HA_Fl2gUAH4sPP2vFcqEHksAi2EGc08vBcOJjRlXmkuXViJoHfq1IRje6tbW9vPFuY4OV14l8Lo1gjSQzK7oBvJUFl5hOH04nS07K1s6WhGAdX2evK0_isDb0MhTbRXF3YDRZJps5-F81DeeKlFZVQioZcxDdAWz5gtEB3kddwq529KdiA91wJqUooVBpVRKsozdK2GHTTe6Tv0CyR9_vEni7erRhpFhqrdXsskptsnbaF_TN6hX60SexSbe--QvWe_UGFZZWDqK_JRf4BH75sDlKlwGMoAoScThAsx658CzR_Q2A6LaXK6xTbzpGdZZ0nb7V9tNJ1epAhlu_JDVUnIIwAViDia05TPEyMZZ7df6lgxnaty8NKkt51Q6_cJH1xJzUuQzjyAOUdovn3_7Zi7zXC0)

A **KafkaProducer** is a **lightweight** client library that applications use to send messages (records) to Kafka topics. It handles networking, serialization, partitioning, batching, retries, and more, while abstracting away the complexities of talking to Kafka brokers.  

### **1️⃣ Establishes Connection to Kafka Brokers**  
- When you create a producer, it connects to one or more **bootstrap servers**.  
- It **fetches metadata** about topics, partitions, and leader brokers.  

### **2️⃣ Serializes Messages Before Sending**  
- Kafka can only store **byte arrays**, so the producer serializes keys and values.  
- Common serializers:  
  - **String → Bytes** (`StringSerializer`)  
  - **JSON → Bytes** (`JsonSerializer`)  
  - **Avro → Bytes** (for schema-based data)  

### **3️⃣ Decides Which Partition to Send Messages To**  
- If a **key** is provided → uses **consistent hashing** to map to a partition.  
- If **no key** is provided → distributes messages using **round-robin** or **sticky partitioning**.  

### **4️⃣ Batches Messages for Efficiency**  
- Instead of sending each message individually, the producer **buffers** messages and sends them in **batches** to reduce network overhead.  
- Configurable via:
  - `linger.ms` (waits before sending to increase batch size)
  - `batch.size` (size of batches in bytes)

### **5️⃣ Compresses Messages to Save Bandwidth**  
- Supports **GZIP, Snappy, LZ4, ZSTD** compression to reduce message size.  

### **6️⃣ Handles Acknowledgments (ACKs) & Reliability**  
- Configurable **ACK levels**:  
  - `acks=0` → Fire-and-forget (fastest but risky).  
  - `acks=1` → Leader ACKs (default, moderate reliability).  
  - `acks=all` → All replicas ACK (strongest reliability).  

### **7️⃣ Handles Retries & Failures**  
- If a broker is down, the producer **automatically retries** sending messages.  
- Configurable via:
  - `retries` → Number of retry attempts.  
  - `retry.backoff.ms` → Time between retries.  

### **8️⃣ Ensures Message Ordering (Per Partition)**  
- Kafka **does not guarantee global ordering**, but messages **within a partition** are **always ordered**.  
- **Using a key ensures all messages with that key go to the same partition**, preserving order.  

### **9️⃣ Asynchronous & High-Throughput**  
- Producers can work in an **async** manner (`send()` method returns immediately).  
- They support **callback functions** to handle success/failure responses.  

---

## **Is Kafka Producer Lightweight?**
✅ **Yes, KafkaProducer is lightweight** because:  
1. It **only maintains a metadata connection** to brokers, instead of holding persistent connections.  
2. It **batches messages** to optimize network usage.  
3. It **operates asynchronously**, minimizing blocking overhead.  
4. It **leverages compression** to reduce message size and improve efficiency.  
5. It **offloads storage & persistence** to Kafka brokers, meaning it doesn’t have to manage messages long-term.  

---

## **Example: Kafka Producer in Python**
```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    key_serializer=str.encode,
    value_serializer=str.encode,
    compression_type='gzip',  # Compress messages
    linger_ms=10,  # Small delay to batch messages
    retries=5  # Retry on failure
)

for i in range(10):
    producer.send('my_topic', key=f'user-{i}', value=f'message-{i}')

producer.flush()  # Ensure all messages are sent before closing
producer.close()
```

## **Key Takeaways**
✅ KafkaProducer **is a lightweight client** that sends messages to Kafka brokers.  
✅ It **handles partitioning, serialization, batching, and retries** automatically.  
✅ It **only establishes a metadata connection**, reducing overhead.  
✅ It is **asynchronous & high-throughput**, making it **efficient for real-time applications**.

---

# Bootstrap server

A **bootstrap server** in Kafka is simply **one or more broker addresses** that a **Kafka client (producer or consumer)** initially connects to in order to **fetch cluster metadata**.  

### **Purpose of a Bootstrap Server**
- It helps clients **discover** the Kafka cluster’s topology (brokers, partitions, leaders).  
- It **does not** handle all communication but acts as an **entry point**.  
- Once metadata is retrieved, the client **caches it** and directly communicates with the relevant brokers.  

### **How It Works in Kafka Producer**
1. The **producer starts** and connects to a **bootstrap server** (e.g., `broker1:9092,broker2:9092`).  
2. The bootstrap server **returns metadata** about the cluster (topics, partitions, leader brokers).  
3. The producer **stores metadata in memory** and uses it to **send messages directly** to the leader broker for a partition.  

### **What Happens if a Bootstrap Server Fails?**
- The client can connect to **any listed bootstrap server** in the configuration.  
- If one fails, it **tries another** until it successfully retrieves metadata.  
- This makes Kafka **fault-tolerant** since any broker can act as a bootstrap server.  

### **Example Kafka Configuration for a Producer**
```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["broker1:9092", "broker2:9092"],  # Bootstrap servers
    acks="all",  # Ensure reliability
    retries=5,  # Retry on failure
)
```
- Here, `broker1` and `broker2` are bootstrap servers.  
- The producer will use **whichever is available** to **fetch metadata** before communicating directly with the leader broker.

### **Key Takeaways**
✅ **Not a special broker** → Any broker can be a bootstrap server.  
✅ **Only used for initial metadata discovery** → Clients don’t keep sending requests to it.  
✅ **Ensures high availability** → Clients switch to another broker if one is down.

---

# So, any broker can act as a bootstrap server. How do all the brokers have consistent metadata?

![](https://plantuml.online/png/ROz1QuD048Nl_eeXfmRI53q6B5IXXsf1qlQIsx9EL69txEv8_dx7LMiikGtxlVVslKvPRdJJASEmIScmfRP52ucb2zeDA0Tf4dItgXnLkLRa_nGZWj339BmBen56QrXOAdiznHPhTYBA43kqJzbHdTbBJbaGnF7K1TweCGx8mYTrZOQqLgP21t4Sf0ayFeiQ3l3LbOeHlf6L70eUS5_jTs3m2luxRiX0wpTk0t68Jzm7UD4NGzSMomgXznbJQX8ABNfN-umvTuRHNJYKdhV2AxAkfUVxN4aA5t_9H_pfqV7YbLTXXKVSMtCpXOVTRhSCaNkSuhPZP3vC-K1JYiiv9LkOG9Erg7cn_G80)

Kafka ensures that **all brokers** in the cluster have consistent metadata through a **centralized controller broker** that manages metadata updates and propagates changes across the cluster.

## **The Role of the Kafka Controller Broker**  
- One broker in the cluster is elected as the **controller** (automatically chosen via ZooKeeper or KRaft in newer versions).  
- The **controller manages all metadata updates** (leader elections, topic changes, broker additions/removals).  
- When metadata changes (e.g., a new topic is created, a broker fails, or a partition leader changes), the **controller updates all brokers**.

## ** Metadata Synchronization Process**
### **Step 1: Metadata Update Happens**
- A change occurs, like:
  - A new topic is created.  
  - A broker joins or leaves the cluster.  
  - A partition leader fails, triggering a new election.  

### **Step 2: Controller Updates the Cluster**
- The **controller broker** detects the change and updates **ZooKeeper (legacy)** or **KRaft (newer Kafka versions)**.  
- The controller **propagates metadata updates** to all other brokers.  

### **Step 3: Brokers Notify Clients (Producers/Consumers)**
- Producers and consumers cache metadata, so they don't need constant broker queries.  
- If they receive an error (e.g., `NotLeaderForPartition`), they request fresh metadata from a broker.

## ** How Clients Fetch Updated Metadata**
- **Producers & consumers fetch metadata from any broker** (since all brokers have the latest metadata).  
- If metadata is outdated or incorrect, the broker returns an error, forcing a **metadata refresh**.  

## ** Ensuring Metadata Consistency**
✅ **Single Source of Truth** → The **controller broker** ensures all brokers stay in sync.  
✅ **Push Model** → The controller proactively **notifies brokers** of metadata updates.  
✅ **Client Auto-Recovery** → If a producer/consumer gets outdated metadata, it requests a **metadata refresh**.

---

# What if the controller fails? 

If the **controller broker** in Kafka fails, Kafka has a **mechanism** in place to handle this situation by **electing a new controller**. Here’s how it works:

### **1️⃣ Controller Failover Process**
- Kafka uses **ZooKeeper** (in older versions) or **KRaft** (in newer versions) to handle **controller failover**.
- If the **controller broker** fails, the remaining brokers in the cluster automatically **detect the failure** and trigger the election of a new controller.
  
#### **Step-by-Step Process (Using ZooKeeper or KRaft)**

1. **Controller Failure Detection**  
   - All brokers in the Kafka cluster are aware of the **controller's status** through **ZooKeeper** or **KRaft**.
   - If the **controller broker fails** (due to crash, network failure, etc.), the brokers **detect the absence** of the controller.

2. **New Controller Election**  
   - In **ZooKeeper-based clusters**, brokers use **ZooKeeper** to elect a new controller.
   - In **KRaft-based clusters** (Kafka without ZooKeeper), the brokers themselves elect a new controller **from the pool of brokers**.
   - The election is based on the current broker state and leader election process.

3. **New Controller Takes Over**  
   - Once elected, the **new controller broker** will:
     - **Re-establish metadata consistency** (by applying any unprocessed metadata changes).
     - **Handle partition leader elections** if necessary (e.g., when a leader broker has failed).
     - **Resume topic creation, replication, and metadata updates**.

4. **Clients (Producers/Consumers) Are Unaffected**  
   - Producers and consumers will not be impacted for long, as they will:
     - **Cache metadata**, and if the cached metadata becomes invalid, they **request updated metadata**.
     - If necessary, they will automatically connect to the **new controller** without needing any manual intervention.

### **2️⃣ Controller Failover in Action**

#### **Example:**
1. **Controller Broker (Broker 1)** fails.
2. The remaining brokers detect the failure and initiate a **controller election**.
3. **Broker 2** is elected as the new controller.
4. **Broker 2** starts managing metadata, leader elections, and topic changes.
5. **Producers and consumers** do not require any manual intervention; they either:
   - Continue working with the **cached metadata**.
   - Request fresh metadata if necessary, which includes the new controller's details.

### **3️⃣ Impact of Controller Failure**
- **Short Period of Unavailability**: The Kafka cluster may experience a short delay (a few seconds) while the new controller is elected.
- **No Data Loss**: The failover process is designed to ensure **no data loss**. Even if a broker fails, Kafka's replication and leader election ensure that no messages are lost.
- **Client Recovery**: Clients will automatically reconnect to the **new controller** and adjust if necessary.

### **4️⃣ Kafka's Fault-Tolerance**
✅ **Automatic Failover**: Kafka automatically handles controller failover, ensuring minimal disruption.  
✅ **Leader Election for Partitions**: If a broker hosting a partition leader fails, Kafka **elects a new leader** for that partition.  
✅ **Metadata Consistency**: The new controller ensures that the metadata is consistent across the entire cluster.

---

# How producer sends the messages
![](https://plantuml.online/png/jLJ1QkCm4BtxA-QO7dBO-1RmGcafkz12QLXw7konBI9BhgHWkb-_8zbMx6oQEeMUR4dptZpDl17cJXjuDheuv6GI3Cj7mY8k7hIKkYFpusIzELcdIP9baGbsf0eBJsGjLWHE3wIGPKcCMVySTxSZ49eZeaNZX1DQ9KFKDFxL23UBbls9r5KGCig21t9vJHRkqI6KHZSJ9V5kC-g0W4POArG5XSUj3BqToBgUG2B_xPNk5EYojEHk9WgFdDjGX860TG4fPmHB2IG38nMH8rRs6zHilgmc_GOrwTLgV4jlSyyhgQWQZWPa_0krKkJeJV9VFwUDk6rR-GwAkZuZswKS_U4DSzu7ntp4YcAYUP-c1LwOPNDLblIqS0kpf8ko-Bh-4bMzVaL7fa6pXpyjyv8lvvcn6mvh3-aY14l-0vprvz98UF5pYakMNHITNeZ-lBqdzpc4Moves6LSUYNEDsC8dmJRuwEwuXBR3AMycRSd1iopTE6DNFcF8nKUIPuqFpUZ1NZ2U9S9uVVknVPZjdjNUMsq4d_xkRghATz_O8V-J9I1GgYrPUn8RW4DyTLyXd2zyuQuqye9TPZPqZDAh2f-OpumnlMeT07g7m00)

When **acks=all** is set, the **leader** will not acknowledge the producer until the message is written to its log and successfully replicated to all **in-sync replicas** (ISRs). The **leader** waits for all the **followers** (or replicas) to acknowledge that they have written the message to their logs before responding to the producer.

1. **Producer sends message to Leader**: The producer sends the message to the leader. 
2. **Leader writes to its log**: The leader writes the message to its log, but does **not** send an acknowledgment yet.
3. **Followers fetch data**: The followers fetch the missing log entries from the leader.
4. **Replication**: Each follower applies the new data to its log and sends an acknowledgment back to the leader, indicating the data has been replicated.
5. **High-watermark update**: The leader updates the high-watermark after receiving acknowledgment from all followers. It then sends the new high-watermark to the followers, and they acknowledge it.
6. **Leader acknowledges producer**: Once the leader has written to its log **and** replicated the message to **all in-sync replicas (ISRs)**, it sends an acknowledgment to the producer. This ensures that the message is safely stored and replicated before acknowledging the producer.
7. **Leader checks ISR**: The leader checks if all in-sync replicas are up to date and continues replication if necessary.

### acks=1:
1. Producer sends a message to the leader.
2. Leader writes the message to its log.
3. As soon as the leader writes the message, it sends an acknowledgment to the producer.

### acks=all:
1. Producer sends a message to the leader.
2. Leader writes the message to its log.
3. The leader waits until the message is replicated to all in-sync replicas.
4. Once replication is complete, the leader sends an acknowledgment back to the producer.


---

# What is partition re-balancing?

Partition rebalancing is the process of redistributing topic partitions across brokers to ensure a balanced workload in the Kafka cluster. This can happen due to various events like **broker failures, new broker additions, or manual reassignments**. The goal is to maintain an even distribution of partitions while ensuring high availability and minimal disruption.

### **Scenarios Triggering Partition Rebalancing**  

1. **New Broker Joins**  
   - When a new broker is added, the Kafka **controller** (one of the brokers that acts as the cluster manager) detects it.
   - To balance the load, Kafka may decide to **move some partitions** from overloaded brokers to the new broker.
   - This is done by updating the **partition leadership** and replica assignments.

2. **Broker Failure or Shutdown**  
   - If a broker fails, its partitions become **unavailable**.
   - Kafka automatically **elects new leaders** from the in-sync replicas (ISR).
   - Once the failed broker recovers, partitions may be reassigned to restore balance.

3. **Manual Partition Reassignment**  
   - Admins can manually trigger a rebalance using Kafka’s **`kafka-reassign-partitions.sh`** tool.
   - This is useful for planned maintenance or performance optimizations.

### **How Partition Rebalancing Works**  

![](https://plantuml.online/png/dLExRiCm3Dpr5HoJeKFHpKC1EsDVGO826G8OYaKxQcL9fUGK_VlASHpP3XgqNSaxadSdMKvU5j9oxM59HZG54hE3OcQCTvwupTT8XqbpORGdezIad2gLPsJUaHnm1saswhueaJyY5qXjiyFbjoF8CtvUGkuOqyOZaAps7amvs9wq3DWTSV1cf7PRlMpdUMaq4EwuuhgGkWBdGzanrck5c_iBYGciyAD1vw56pmNtd4qXBQqVqS9zG_gCXfbH0knvlzIbcOzNHWyIMACMWUiShn1caRQPiu5LeuNfuW5cwwOe0cj-pPPemWPgSq07tWpyZD2Z3wTwcE-ShFIGpVgSni0LMYKBxbjhXxkEfatkYgmXicoK-WeHTNDG_7nKa5-t0uE2pfC9CiqIUBLXCyRSVfbpSwI9V-Ujm-jJfpZxWoU9HnrNykv1VqWxmfwwaU7BKJ09Qsk8ampcEWnVAhZMlihkogrkj9SgAf0kH50IkZsARm00)

#### **Step 1: Controller Detects Change**
- The **controller broker** (a special Kafka broker that manages cluster state) **detects** a new broker or a failure event.
- It starts the **partition reassignment** process and determines how partitions should be redistributed.

#### **Step 2: New Partition Mapping is Created**
- The controller generates a new partition mapping to ensure an even distribution of partitions across brokers.
- **Constraints considered:**
  - Each partition should have a leader and replicas spread across different brokers.
  - Followers should not reside on the same broker as the leader.
  - Minimize unnecessary partition movement to reduce downtime.

#### **Step 3: Partition Movement Begins**
- Kafka reassigns partitions by updating **Zookeeper (or KRaft in newer versions)** with the new partition assignments.
- The **newly assigned followers** start fetching data from the existing leader.
- Once fully caught up, the leader role may shift to balance the cluster.

#### **Step 4: Leadership Handover (If Needed)**
- Kafka may shift leadership of partitions to reduce load on overloaded brokers.
- The controller updates the metadata about new partition leadership.
- Producers and consumers get updated **metadata** and send requests to the new leader.

---

### **Summary**  
- **Partition rebalancing ensures even distribution of partitions** when brokers join or leave.  
- The **Kafka controller orchestrates the reassignment** and updates metadata.  
- **Producers and consumers refresh metadata** to adapt to the new partition layout.  
- **Temporary performance degradation** may occur due to the extra data movement.

### **Key Takeaways:**
1. **Before Rebalancing**  
   - The producer fetches **metadata** from the bootstrap server.  
   - It sends messages to the **old leader** (Broker 1) of **Partition X**.  

2. **During Rebalancing**  
   - The controller assigns **Partition X** to the **new broker (Broker 3)**.  
   - Broker 3 **fetches data** from the old leader.  

3. **After Rebalancing**  
   - The controller **promotes** Broker 3 to the **new leader**.  
   - **Metadata updates** are propagated to all brokers.  
   - The producer **refreshes metadata** and starts sending messages to **Broker 3**.  

#### **What Happens to Producer Messages?**
- **Until metadata refresh**, messages are still sent to the **old leader** (Broker 1).  
- If the producer tries to send a message to the old leader **after it loses leadership**, it will receive an error and **retry after fetching updated metadata**.

# Failure recovery at Kafka (E.g. If the leader suddenly crashes)

![](https://plantuml.online/png/dLDBJyCm3BxdL_Yu7ZZ0RZqWRKD821ZJAYGEawQezTPeML9Ybx5_Jy8UQJDDGboTp_uUTXhfM9MgaOPXvcpLbkX4qocEhMLY9vjbWUuhUPnOmyvgdPH7MY_7pcxG4KY2qRZt-gQhvGlA2bruFE2Mjpt8evzfTw7SWTpr85FSNKuP2c4i8pYrhXdigiELdvbWSAXai99A4xG6lnii6Ikz5-8K0jpSNtZFOOwVBHB35bbMagL88Q7jD2B0kNNcZ8Q1rHNeH4_M9-rABj1Klfj8hX46is2VbJNmaObEYZtAgGM7r5X3lYCOR1rcQInnRpay87lpSH5mR5gOWZqX7VK2QW_pv4B4xa0TTvN3fCPo0q_578WbjvH0uyxoe7WRD9qs1soFJ4dJQ9p3U-FZmvXwOYUwVpqbJQoqXiOguntuqJ7uXV5RSNi_hAobKRGDMhtFlww-_TLI_Vi43ExI4nWc9z3DQOvq_GWwdw17Efeymw1eoz9tPTVJEdCIogtsMBttnyDE8S5ESGrHg_W1)

### **Key Steps in Failure Recovery**
1. **Leader Fails**  
   - The producer was sending messages to **Broker 1 (Old Leader)**.  
   - Broker 1 **crashes or becomes unreachable**.  

2. **Leader Election Process**  
   - The **Kafka Controller** detects failure and starts **leader election**.  
   - It checks the **In-Sync Replicas (ISR)** to find a new leader.  
   - **Broker 3** is promoted as the **new leader** for **Partition X**.  
   - Metadata updates are **propagated to all brokers**.  

3. **Producer Retries and Updates Metadata**  
   - The producer **receives no response** from Broker 1 and triggers a **retry mechanism**.  
   - It **requests updated metadata** from the bootstrap server.  
   - The bootstrap server responds with **Broker 3 as the new leader**.  
   - The producer **resends the message to Broker 3**, ensuring **no message loss**.

### **Key Takeaways**
✔ **Automatic Recovery:** Kafka **self-heals** by promoting a new leader.  
✔ **Seamless Producer Handling:** Producers **retry and fetch updated metadata** before resending.  
✔ **No Data Loss:** If the producer has **acks=all**, Kafka ensures that the message is replicated before acknowledging.

This ensures **fault tolerance and high availability** in Kafka. 🚀