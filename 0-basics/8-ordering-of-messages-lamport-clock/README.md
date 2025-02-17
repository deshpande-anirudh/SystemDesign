# Hybrid logical clock

![](https://plantuml.online/png/bP9VJW8n48VVUue9BqA22TtwXoN1X6rqVT0dlK33LjW4jvksW5x00tX4Js9Bkq0BDV6ndM-cl_bsMoPrFQzRrcYOeVReL69W2debqtpBFW7tmceMLBEeIe8g2QilN6wut15K25dL3TErQFnzo1R1YI9q0JDGlAaKC7ZdIh451osWrWeM_hb-YGTe1fTtPeU9cTfKSB_XTa4C_TSf7es6GAUZ0J8hTf0Maflw49xPHyUin9ojfldr07w-lizrki0JU11oosHrCj-4zRksKinDM6vIcpHlZbUsmMItBirjIP2dZqQVnhaz4-VGLsP-upZB4K8IY8bRdBfTIh5UBCrWL0GFEAN5RaQUTrwoZd71RS7dljhdZkZOOZJo877TLkOBAtXyebQX1QqtbxZMVzlByzWR3gHqVqg1amX982OXJNiZY0RTpXjrIuux4wHZlBVntjlDmLj8nzwYaMblz5_Unh6txAmtYfD8ba1-0G00)

Here's a **README** that explains the **Hybrid Logical Clock (HLC)**, how it works, and how to use it in a distributed system.

---

# **Hybrid Logical Clock (HLC)**

## **Overview**
A **Hybrid Logical Clock (HLC)** is a mechanism designed to provide **causal ordering** of events in **distributed systems**. It combines the benefits of both **physical time** (based on system clocks) and **logical time** (based on a counter) to ensure events are correctly ordered across nodes, even when physical clocks are not perfectly synchronized.

HLC is widely used in systems like distributed databases, messaging platforms (e.g., Slack), and event-driven architectures.

## **Why HLC?**
In distributed systems, maintaining a **global order** of events is crucial, but it can be difficult due to:
1. **Clock skew** between different machines.
2. **Network delays** in message transmission.

HLC addresses these issues by:
- **Combining logical clocks** to track causal relationships.
- **Using physical time** to align events with real-world time.

## **Components of HLC**
An HLC timestamp consists of two components:
1. **T (Physical Time)**: The time derived from the system’s clock.
2. **C (Logical Counter)**: A counter that is incremented if multiple events share the same physical timestamp.

The HLC timestamp is represented as `(T, C)`.

## **How It Works**
### **Generating a New Event**
- When a new event is generated locally, the timestamp is set as:
  ```
  T_new = max(T_local, physical_time)
  ```
- If the timestamp advances (`T_new > T_local`), the counter `C` is reset to 0.
- If the timestamp is the same as the last event (`T_new == T_local`), the counter `C` is incremented.

### **Receiving an Event**
- When a node receives an event with a timestamp `(T_recv, C_recv)`:
  - The timestamp is updated to the maximum of:
    ```
    T_new = max(T_local, T_recv, physical_time)
    ```
  - If `T_recv == T_local`, the counter `C` is incremented:
    ```
    C_new = max(C_local, C_recv) + 1
    ```
  - If `T_recv > T_local`, the counter `C` is reset to 0.

This combination of physical and logical time ensures that events are ordered correctly, even if they are generated or received at different times or locations.

## **HLC Pseudocode**

```python
class HLC:
    def __init__(self):
        self.T = get_physical_time()  # Get current system time
        self.C = 0  # Initialize logical counter

    def get_physical_time():
        return current_system_time_in_milliseconds()  # Use UTC time

    def generate_event(self):
        """ Generates a new event and assigns a timestamp """
        new_T = max(self.T, get_physical_time())
        if new_T > self.T:
            self.C = 0  # Reset counter if physical time advances
        else:
            self.C += 1  # Increment counter for same timestamp
        self.T = new_T
        return (self.T, self.C)

    def receive_event(self, T_recv, C_recv):
        """ Receives an event with timestamp and updates the local clock """
        new_T = max(self.T, T_recv, get_physical_time())
        
        if new_T == self.T and new_T == T_recv:
            self.C = max(self.C, C_recv) + 1  # Increment counter for same timestamp
        elif new_T == self.T: 
            self.C += 1  # Increment counter for same local timestamp
        else:
            self.C = 0  # Reset counter if physical time advances
        
        self.T = new_T
        return (self.T, self.C)  # Return updated timestamp
```

## **Functions**

### `get_physical_time()`
Returns the current system time in milliseconds using the system clock (UTC time). It ensures consistency across distributed systems by using a monotonic clock.

### `generate_event()`
Generates a new event and assigns it a timestamp based on the local system time and logical counter. It ensures that the timestamp is correctly ordered even if multiple events occur at the same physical time.

### `receive_event(T_recv, C_recv)`
Handles the receipt of an event and updates the local timestamp. It ensures that events are ordered correctly and maintains causal consistency across nodes.

## **Usage Example**

```python
# Initialize HLC for the system
hlc = HLC()

# Generate a new event
event_A = hlc.generate_event()  # Output: (T=100, C=0)
print(f"Event A Timestamp: {event_A}")

# Receive an event from another node
event_B = hlc.receive_event(100, 0)  # Output: (T=100, C=1)
print(f"Event B Timestamp: {event_B}")
```

## **Why Use HLC?**
1. **Causal Ordering**: Ensures that events are ordered in a way that respects causal relationships.
2. **Fault Tolerance**: Works even with **clock skew** and network delays.
3. **No Global Clock**: Avoids the need for a centralized, synchronized clock.

## **Applications of HLC**
- **Distributed Databases** (e.g., CockroachDB, Cassandra): Ensures consistency across nodes without requiring synchronization of physical clocks.
- **Event-Driven Systems** (e.g., Slack, Kafka): Orders events correctly across different services.
- **Message Queues**: Manages the ordering of messages in distributed messaging systems.

---

### **Conclusion**
The **Hybrid Logical Clock (HLC)** is an effective way to manage event ordering in distributed systems. By combining **logical counters** with **physical timestamps**, it handles clock skew and network delays while ensuring causal consistency. Whether you’re building distributed databases, messaging systems, or any real-time application, HLC provides a reliable method for managing event order without relying on strict clock synchronization.
