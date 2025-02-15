# Preventing phantom reads

## 2 Phase locking
![](https://plantuml.online/uml/bP712i8m343l_OfuKz31UXGcE1Kl7WGddakDMjoQqdRg3tZp4_Jd_18hU71EPDuIyfAyj4POhwGoGdl8OcRUKrv9nobZMGozGOZwC2EvXo6qfvQEIczXlXCEEopZ5I2j0_4di1BA1o2Aebhxi5hLv17eW3QOTeDU7yOerlcJ92bBwrfmlrqOIn9Ob5AYSvioXya9PUaLwH29mkG8ITBWaBZn8NEq6x85a44hdelSMt6fyzU2nSuglVywuGMbFw4H5ONoSB-UsPTt-liV-2zztaIVDz7dTVq7)

## Serializable snapshot isolation

### **Serializable Snapshot Isolation (SSI)**
Serializable Snapshot Isolation (SSI) is an advanced concurrency control mechanism that **extends Snapshot Isolation (SI) to ensure true serializability** without traditional **two-phase locking (2PL)**. It eliminates anomalies like **write skew** and **phantom reads** while maintaining high performance.

---

### **How It Works**
1. **Reads From a Snapshot**  
   - Each transaction sees a **consistent snapshot** of the database at the start of execution.
   - No locks are acquired on read, unlike **2PL**.
   
2. **Detects Conflicts Instead of Blocking**  
   - Instead of blocking writes (like in 2PL), SSI **detects conflicts dynamically** using dependency tracking.
   - If conflicts occur, the system **aborts one of the transactions** to maintain serializability.

3. **Key Conflict Scenarios**
   - **Write-Write Conflict:** Two transactions updating the same row → **One must abort**.
   - **Read-Write Conflict (Write Skew):** A transaction reads a value and another transaction **modifies it before committing** → **One must abort**.
   - **Phantom Read Conflict:** A transaction reads a range, while another transaction **inserts/deletes** within that range → **One must abort**.

---

### **Example of Write Skew (Prevented by SSI)**
#### **Scenario (Hospital Shift Example)**
- A hospital requires **at least one doctor on duty**.
- Two doctors, **T1 and T2**, decide to **take a leave** at the same time.

#### **Execution Without SSI (Anomaly)**
1. **T1 Reads:** "There is 1 doctor on duty."
2. **T2 Reads:** "There is 1 doctor on duty."
3. **T1 Updates:** "Set myself as off-duty."
4. **T2 Updates:** "Set myself as off-duty."
5. **Both Commit:** ❌ **Now, 0 doctors are on duty!**

#### **Execution With SSI**
1. **T1 Reads:** "There is 1 doctor on duty."
2. **T2 Reads:** "There is 1 doctor on duty."
3. **T1 Updates:** "Set myself as off-duty."
4. **T2 Tries to Commit:** ❌ **Conflict detected! T2 is aborted.**
5. **Only T1 Commits.** ✅  
   - The hospital **still has one doctor on duty**.

---

### **How SSI Prevents Phantom Reads**
Instead of **locking** ranges like **Predicate Locking in 2PL**, SSI **tracks read and write dependencies**:
- If a transaction **reads a range**, and another transaction **inserts or deletes** in that range → **The second transaction is aborted**.

This ensures that transactions appear **as if they executed sequentially**, preserving serializability.

---

### **Advantages Over 2PL**
✅ **No locks, higher concurrency**  
✅ **No deadlocks** (since transactions don’t wait, they just retry)  
✅ **Better for read-heavy workloads**  

### **Disadvantages**
❌ **Abort-heavy**: Transactions can be **rolled back often** due to conflict detection.  
❌ **More complex implementation** than traditional SI or 2PL.  

---

### **Summary**
- SSI **extends Snapshot Isolation** by **detecting and aborting conflicting transactions**.
- Prevents **write skew, phantom reads, and serializability anomalies** **without locking**.
- Ideal for **high-concurrency, read-heavy systems** (e.g., distributed databases).

# How SSI works behind the scenes? 

### **How Serializable Snapshot Isolation (SSI) Works Behind the Scenes**  

Serializable Snapshot Isolation (SSI) **extends traditional Snapshot Isolation (SI)** by **detecting conflicts dynamically** instead of using locks. It ensures that transactions execute in a way that is equivalent to some serial order.

---

## **1. Core Mechanisms Behind SSI**
### **A. Reads from a Consistent Snapshot**
- Each transaction reads from a **consistent snapshot of the database**, meaning:
  - It sees only committed data at the time the transaction **started**.
  - It does **not** block other transactions.
  - It **ignores concurrent uncommitted writes**.
  
✅ **Benefit**: No locks on reads → higher concurrency.

---

### **B. Conflict Detection Instead of Locking**
Unlike **2PL**, SSI does not block conflicting transactions. Instead, it **tracks dependencies between transactions** and aborts those that would violate serializability.

#### **Two Key Conflict Types:**
1. **Write-Write Conflicts** (**WW Conflicts**)  
   - Two transactions try to **update the same row**.  
   - **Resolution**: The system **aborts one of them**.  
   - **How?** By tracking modified rows in an **in-memory conflict table**.

2. **Read-Write Conflicts** (**RW Conflicts / Write Skew / Phantom Reads**)  
   - A transaction **T1 reads** some data while **T2 modifies it** before T1 commits.  
   - **Resolution**: The system **tracks dependencies** and **aborts one transaction** if necessary.

✅ **Benefit**: No need for range locks (as in 2PL), allowing higher concurrency.

---

## **2. Internal Components**
### **A. Versioned Data Storage**
- The database **stores multiple versions** of a row (Multi-Version Concurrency Control, MVCC).
- Each version is timestamped based on the **transaction that wrote it**.
- Transactions always read the **latest committed version** that was valid at their **start time**.

✅ **Benefit**: Readers don’t block writers & vice versa.

---

### **B. Conflict Tracking (Dependency Graph)**
- The database tracks dependencies between transactions using a **conflict graph**.
- The graph is used to **detect cycles**, which indicate serializability violations.

#### **Example Conflict Graph**
```
T1 → T2 → T3 → T1  (Cycle detected! Must abort one transaction)
```
- If **no cycles exist**, transactions can commit.
- If a cycle is found, **one transaction is aborted** to break it.

✅ **Benefit**: No explicit locks, reducing contention.

---

## **3. Phantom Read Prevention in SSI**
Phantom reads happen when a transaction reads a **set of rows**, but another transaction **inserts or deletes rows** in that set before the first transaction commits.

### **How SSI Prevents Phantom Reads:**
1. **Tracking Range Queries**  
   - Instead of locking ranges (like in 2PL), **SSI remembers which ranges a transaction read**.
   
2. **Checking for Conflicts**  
   - If another transaction **modifies that range** (e.g., inserts a new row that should’ve been read), SSI detects a **RW conflict**.

3. **Abort & Retry**  
   - If a transaction would lead to a serializability violation, **one transaction is aborted**.

✅ **Benefit**: Prevents phantom reads **without locking**.

---

## **4. Comparison: SSI vs. 2PL**
| Feature                | Two-Phase Locking (2PL) | Serializable Snapshot Isolation (SSI) |
|------------------------|----------------------|--------------------------------|
| **Locking Mechanism** | Uses locks (shared/exclusive) | No locks, tracks conflicts |
| **Concurrency** | Low (blocking) | High (non-blocking) |
| **Phantom Read Prevention** | Uses range locks | Tracks range conflicts dynamically |
| **Deadlocks** | Possible | No deadlocks |
| **Rollback Rate** | Low | High (due to aborts) |
| **Performance** | Slower for reads | Faster for reads |

---

## **Summary**
✅ **Reads from a snapshot (MVCC)** → No blocking  
✅ **Tracks dependencies using a conflict graph** → Detects cycles  
✅ **Prevents write skew & phantom reads** → Without range locks  
✅ **Higher concurrency than 2PL** → But may have more aborts  

# Durability

### **How Durability is Achieved in Data Systems**  

**Durability** (the **D** in **ACID**) ensures that once a transaction is committed, its changes **persist permanently**, even in the event of a system crash, power failure, or hardware failure.  

---

## **1. Write-Ahead Logging (WAL)**
- Before modifying data, the system **first writes the change to a log** (typically on disk).
- If a crash happens before the actual data is written, the system can **replay the log** to restore the changes.

✅ **Example:**
1. A transaction updates `balance = balance - $50`.
2. The change is **written to a log** (WAL).
3. Only after logging, the database updates the actual table.
4. If a crash happens after logging but before writing to the table, the database **replays the log** to ensure durability.

📌 **Used In:** PostgreSQL, MySQL (InnoDB), Oracle, MongoDB.

---

## **2. Replication (Synchronous & Asynchronous)**
Replication **copies data to multiple nodes** to ensure durability.

### **A. Synchronous Replication**  
- The transaction **does not commit** until at least one replica has the data.  
- If the primary node crashes, a replica takes over with **zero data loss**.  

✅ **Stronger durability**, but **higher latency**.

📌 **Used In:** **CockroachDB, Google Spanner (Paxos), Amazon Aurora**.

### **B. Asynchronous Replication**  
- The transaction commits **immediately** and data is sent to replicas **afterward**.
- If the primary node crashes before replication completes, **some data may be lost**.

✅ **Faster commits**, but **possible data loss**.

📌 **Used In:** **MySQL Replication, MongoDB Replica Sets (eventual consistency)**.

---

## **3. Checkpointing**
- The database **periodically saves a consistent snapshot** of its state.  
- If a crash happens, the system can **recover from the last checkpoint + WAL logs**.

✅ **Faster recovery**, since it doesn't need to replay the entire WAL from the beginning.

📌 **Used In:** PostgreSQL, HDFS, Apache Flink.

---

## **4. Distributed Consensus (Paxos/Raft)**
- In distributed databases, consensus protocols (Paxos, Raft) ensure durability by **replicating logs across multiple nodes**.
- A write is committed only when a majority (**quorum**) of nodes agree on it.

✅ **Strong durability & consistency** in distributed systems.

📌 **Used In:** **Google Spanner (Paxos), Etcd, Apache Kafka (Raft), Amazon DynamoDB (Raft-based streams).**

---

## **5. Storage-Level Durability (fsync, SSDs, Write Barriers)**
- Databases **force disk writes** using `fsync()` to ensure changes are physically stored on disk.
- **Journaling file systems** (e.g., ext4, NTFS) also guarantee metadata consistency.

✅ Prevents data loss due to OS crashes.

📌 **Used In:** PostgreSQL (`fsync`), MongoDB (`journal` mode), Linux `ext4` journaling.

---

## **Summary**
| **Method**                | **How it Ensures Durability** |
|--------------------------|-----------------------------|
| **Write-Ahead Logging (WAL)** | Logs changes before writing data, enabling recovery. |
| **Replication** | Copies data to replicas (synchronous = strong, async = eventual). |
| **Checkpointing** | Periodically saves snapshots for faster recovery. |
| **Consensus Protocols (Raft/Paxos)** | Ensures agreement across distributed nodes before committing. |
| **Storage-Level Durability (fsync, SSDs, Journaling FS)** | Forces disk writes to prevent OS crashes from losing data. |


