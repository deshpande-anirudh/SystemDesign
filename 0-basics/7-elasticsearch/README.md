# Is Elasticsearch in-memory? 

No, Elasticsearch is **not purely in-memory**. It is a **disk-based** search engine, meaning that it stores most of its data on disk, but it **caches frequently accessed data** in memory for better performance. Here's a breakdown of how Elasticsearch handles data storage:

### **1. Disk-based Storage**
Elasticsearch primarily stores its data on disk in the form of **indexes**, which consist of **shards** and **replicas**. Each shard is a self-contained index that contains documents, and Elasticsearch uses various data structures on disk to store, index, and manage the data efficiently. These structures include:

- **Inverted Indexes**: For fast text search operations.
- **Data Structures for Storing Documents**: Elasticsearch uses Lucene internally to store and manage document data.
- **Transaction Log (Translog)**: To ensure durability and to recover data in case of failure. Every operation (like indexing a document) is first written to the translog before being committed to disk.

### **2. In-memory Caching**
While the data itself is stored on disk, Elasticsearch uses various memory structures to improve performance:

- **Field Data Cache**: Stores field data in memory for faster access during search queries, such as for sorting or aggregations. These are usually loaded into memory for better query performance.
  
- **Query Caches**: Caches the results of frequent queries in memory so that Elasticsearch can serve subsequent requests for the same query more quickly.

- **File System Cache**: Elasticsearch relies on the operating system’s file system cache to keep frequently accessed portions of the index in memory. This is a performance optimization that reduces disk I/O.

- **Heap Memory**: Elasticsearch uses **JVM heap memory** for managing these memory structures (like caches) and for running the garbage collector. The heap size is configurable but is limited by the physical memory of the system.

### **3. Hybrid Approach**
Elasticsearch uses a **hybrid approach**, where:
- **Data is stored on disk** for durability and scalability.
- **Frequently accessed data** is cached in memory to improve performance, particularly for search and aggregations.
  
This ensures that Elasticsearch can scale well to handle large datasets (storing them on disk) while still providing fast access to frequently queried data (using memory).

### **Conclusion**
- **Not purely in-memory**: Elasticsearch stores its primary data on disk for persistence.
- **Efficient caching**: Frequently accessed data is cached in memory to optimize performance.

This combination of disk-based storage and in-memory caching helps Elasticsearch provide a balance between scalability and speed.

# Primary term, sequence number for optimistic concurrency control

In Elasticsearch, **`primary_term`** and **`seq_no`** are part of the internal versioning system used for **optimistic concurrency control**. They help track the changes made to a document in a specific shard and ensure that updates or deletes are done with the most recent version of a document. Here's an explanation of both:

### **1. `seq_no` (Sequence Number)**

- **Definition**: The `seq_no` (sequence number) is a unique number assigned to each operation (such as an index, update, or delete) on a document within a shard. Every time an operation is performed on a document, the `seq_no` increases, meaning that newer operations have a higher sequence number than older ones.
  
- **Purpose**: The `seq_no` ensures the order of operations in Elasticsearch. It's used to guarantee that you are performing an update or delete operation on the most recent version of a document.

- **Usage**: When performing an **update** or **delete** operation, you can use the `seq_no` and `primary_term` to ensure you're operating on the latest version of the document. If another operation on the same document occurs between your fetch and update, a conflict will occur because the `seq_no` will have changed.

- **Example**: 
  - Document 1 gets indexed — it has `seq_no = 1`.
  - Another update happens — the document gets a new `seq_no = 2`.
  - A conflict will occur if you try to update with the old `seq_no` (e.g., `seq_no = 1`), because Elasticsearch expects the latest `seq_no = 2`.

### **2. `primary_term`**

- **Definition**: The `primary_term` is used in conjunction with the `seq_no` to provide a versioning mechanism that is consistent across all replicas of a shard. The `primary_term` is incremented each time the **primary shard** of a document is promoted, usually during a **primary shard failover**.

- **Purpose**: The `primary_term` helps in situations where the **primary shard** of a document may be reassigned (for example, due to a node failure). It ensures that you are working with the correct version of the document in a replicated environment, taking into account the possible failover of the primary shard. This prevents conflicts that could occur if replicas fall behind after a primary shard promotion.

- **Usage**: When you perform a versioned operation like **update** or **delete**, Elasticsearch checks both `seq_no` (to check the order of operations) and `primary_term` (to check that the operation is being performed on the correct shard version). If these values don't match, it will result in a conflict error.

- **Example**:
  - A document initially resides on primary shard 1 and has `primary_term = 1`.
  - If the primary shard of this document is reassigned to another node due to failure, the `primary_term` will increment (e.g., `primary_term = 2`).
  - If you attempt to update the document using the older `primary_term = 1` after the failover, Elasticsearch will detect the conflict.

### **How `seq_no` and `primary_term` Work Together**

When performing an **update** or **delete**, Elasticsearch uses both **`seq_no`** and **`primary_term`** to ensure that the operation is executed on the **latest** version of the document. Here's how:

1. **When you fetch a document**: Elasticsearch returns both the `seq_no` and `primary_term` associated with that document.
2. **When you perform an update or delete**: You can include the `seq_no` and `primary_term` in the request to ensure that the operation is performed only if the document has not been modified since you fetched it.
   - If the `seq_no` or `primary_term` has changed (i.e., someone else updated the document), Elasticsearch will throw a **`ConflictError`** because the version information has changed, indicating that the document has been modified between your fetch and your update.

### **Example of Conflict Resolution**

Let's say you are working with a document with `seq_no = 1` and `primary_term = 1`:

- **Initial State**:
  - `seq_no = 1`
  - `primary_term = 1`

1. You fetch the document and get the `seq_no` and `primary_term`.
2. In the meantime, another user updates the document:
   - The document now has `seq_no = 2` and `primary_term = 1` (still the same primary term).
3. You attempt to update the document with your **old** `seq_no = 1` and `primary_term = 1`.
   - Elasticsearch detects a mismatch in `seq_no`, because the document has been updated in the meantime, and throws a **`ConflictError`**.
4. You can handle this conflict by fetching the document again, obtaining the updated `seq_no` and `primary_term`, and retrying the update with the new values.

### **Summary**

- **`seq_no`** tracks the order of operations on a document in a specific shard.
- **`primary_term`** tracks the primary shard version and ensures consistency in case of failovers.
- Together, they provide **optimistic concurrency control**, allowing Elasticsearch to manage concurrent updates and prevent conflicts by verifying the document’s version before performing operations like updates or deletes.

