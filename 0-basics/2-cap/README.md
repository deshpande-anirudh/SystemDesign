### **How CAP Consistency is Achieved in Distributed Systems**  

The **CAP theorem** states that a distributed system can only achieve **two out of three** properties at a time:  
- **C** → **Consistency** (Every read gets the latest write)  
- **A** → **Availability** (Every request gets a response, even during failures)  
- **P** → **Partition Tolerance** (System continues working despite network failures)  

Since distributed systems **must be partition tolerant (P)** in a real-world scenario, they must choose between:  
1. **CP (Consistency + Partition Tolerance)** → Sacrifices availability  
2. **AP (Availability + Partition Tolerance)** → Sacrifices consistency  

### **How CP Systems Ensure Consistency**
CP systems prioritize **strong consistency**, ensuring all nodes always agree on the latest data.

#### **1. Synchronous Replication**
- Writes are **only committed when all replicas confirm the update**.
- If a partition happens, nodes may become **unavailable** rather than returning stale data.

✅ **Guarantees consistency but reduces availability.**  
📌 **Examples:** Google Spanner, Zookeeper, Amazon DynamoDB (with Strongly Consistent Reads)

---

#### **2. Quorum-Based Writes (Paxos/Raft)**
- A transaction is considered committed only when **a majority of nodes acknowledge it**.  
- If fewer than a quorum are available, the system **rejects writes** rather than risking inconsistency.  

✅ **Ensures consistency by requiring majority agreement.**  
📌 **Examples:** Etcd, Apache Kafka (Raft), Google Spanner (Paxos)

---

#### **3. Linearizability (Strict Serializability)**
- **All reads return the latest committed value**, even across partitions.  
- Achieved by **global clocks** (Google Spanner uses TrueTime) or **distributed locking**.

✅ **Ensures each transaction appears instantaneously.**  
📌 **Examples:** Google Spanner (TrueTime), FoundationDB  

---

### **How AP Systems Provide Eventual Consistency**
AP systems focus on **availability** but allow temporary inconsistencies. They use **mechanisms to eventually sync data** across nodes.

#### **1. Eventual Replication**
- Writes are **accepted immediately** and propagated to other nodes **asynchronously**.
- Reads may return **stale data**, but the system will **eventually** become consistent.

✅ **High availability but temporary inconsistency.**  
📌 **Examples:** Amazon S3, Cassandra (default mode), DynamoDB (eventual reads)

---

#### **2. Conflict Resolution (CRDTs, Version Vectors)**
- When nodes diverge (e.g., due to network partitions), systems resolve conflicts:
  - **Last Write Wins (LWW)**
  - **Mergeable Data Structures (CRDTs)**
  - **Vector Clocks (DynamoDB)**

✅ **Ensures eventual consistency without blocking writes.**  
📌 **Examples:** Riak, Amazon DynamoDB, Cassandra

---

### **Comparison of CP vs. AP**
| Feature | **CP (Consistency + Partition Tolerance)** | **AP (Availability + Partition Tolerance)** |
|---------|--------------------------------|--------------------------------|
| **Availability** | Low (may reject requests) | High (always responds) |
| **Consistency** | Strong (always latest data) | Eventual (may return stale data) |
| **Write Handling** | Slow (must wait for consensus) | Fast (writes accepted immediately) |
| **Failure Behavior** | System may become unavailable | System keeps running but with inconsistent data |
| **Examples** | Spanner, Etcd, Zookeeper | DynamoDB, Cassandra, Amazon S3 |

---

### **Summary**
- **CAP Consistency (CP) is achieved through synchronous replication, quorum-based writes, and linearizability.**  
- **Eventual consistency (AP) is achieved through asynchronous replication and conflict resolution techniques.**  
- **Real-world systems often allow tuning** between strong and eventual consistency depending on the use case.
