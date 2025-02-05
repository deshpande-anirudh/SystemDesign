# Functional requirements

Above the line:
1. User should be able to search for events
2. User should be able to view events
3. User should be able to book tickets for events

Below the line: 
1. User should be able to get confirmation, reminders
2. User should be able to sign-up for future event notifications at the same venue
3. User should be able to get recommendations on similar future events
4. Adhere to GDPR 


# Non-functional requirements
1. Prioritize availability over consistency on search and view events, consistency for booking tickets
2. Low latency (< 500ms) for all operations
3. Read to write ratio: 100:1


--------

# Concepts

Refer to this link for additional details: 
https://github.com/deshpande-anirudh/SystemDesign/tree/main/1-basics 

## ACID
### Atomicity: 
Abortability of a transaction. Either commit all queries in a transaction, or nothing.

### Consistency:
- The database is kept in consistent state before and after the transaction. 
- Integrity and referential integrity constraints are fulfilled. 

### Isolation:

*Read uncommitted*: Concurrent reads can read uncommitted values
- E.g. T1: Set name to Alice, T2: read Alice, T1 commit, T2 commit

*Read committed (No dirty reads)*: Concurrent modifications to the same row, only 1 will succeed
- E.g. T1: Set name to Alice, T2: `Read None`, T1 commit, T2 commit

*Repeatable reads*: 
- Long-running transaction, same row is read twice -> reads will be consistent
  - Achieved through Multi-version concurrency control

*Serializable*:
- Concurrent transactions execute as if one executes after another
- Low performance

### Durability: 
- Data is preserved even if the database crashes (Redundancy, Leader-Follower architecture)


## CAP theorem
In a distributed system, only 2 out of 3 is achievable (Consistency, Availability and Partition tolerance)

---

# Database design

#### 1. **Events Table**  
Stores information about events like concerts or shows.  
```sql
CREATE TABLE Events (
    EventID BIGINT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    StartDate DATETIME NOT NULL,
    EndDate DATETIME NOT NULL,
    VenueID BIGINT NOT NULL,
    FOREIGN KEY (VenueID) REFERENCES Venues(VenueID)
);
```

#### 2. **Venues Table**  
Stores details of event venues.  
```sql
CREATE TABLE Venues (
    VenueID BIGINT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Location VARCHAR(500) NOT NULL,
    Capacity INT NOT NULL
);
```

#### 3. **Tickets Table**  
Represents tickets for specific events, linked to seat information if applicable.  
```sql
CREATE TABLE Tickets (
    TicketID BIGINT PRIMARY KEY,
    EventID BIGINT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    SeatNumber VARCHAR(50) DEFAULT NULL,
    TicketStatus ENUM('AVAILABLE', 'BOOKED', 'CANCELLED') DEFAULT 'AVAILABLE',
    FOREIGN KEY (EventID) REFERENCES Events(EventID)
);
```

#### 4. **Bookings Table**  
Tracks bookings made by users for specific tickets.  
```sql
CREATE TABLE Bookings (
    BookingID BIGINT PRIMARY KEY,
    UserID BIGINT NOT NULL,
    TicketID BIGINT NOT NULL,
    BookingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    PaymentStatus ENUM('PENDING', 'COMPLETED', 'FAILED') DEFAULT 'PENDING',
    FOREIGN KEY (TicketID) REFERENCES Tickets(TicketID)
);
```

### **Additional Considerations**  
1. **Indexes:** Add indexes for faster search on `EventID`, `VenueID`, and `BookingID`.  
2. **Scalability:** You may shard tickets and bookings based on EventID for large-scale systems.  
3. **Concurrency:** Ensure strong transactional guarantees when updating ticket statuses to avoid double bookings.  
4. **Optional Table for Payments:** To track payment details separately if required.

-----

# Initial state of the system

To set up the initial state for our system with an event at **Dodgers Stadium**, we would need to populate the database with the following entities:

---

### **1. Insert Venue (Dodgers Stadium)**

```sql
INSERT INTO Venues (VenueID, Name, Location, Capacity) 
VALUES (1, 'Dodgers Stadium', 'Los Angeles, CA', 56000);
```

---

### **2. Insert Event (Example: Concert at Dodgers Stadium)**  
Assume the event is a concert scheduled for a specific date.

```sql
INSERT INTO Events (EventID, Name, Description, StartDate, EndDate, VenueID) 
VALUES (1, 'Dodgers Stadium Concert', 'A grand concert featuring famous artists.', '2025-04-01 20:00:00', '2025-04-01 23:00:00', 1);
```

---

### **3. Insert Tickets for the Event**  
For simplicity, we’ll assume we’re selling general tickets with seat numbers. If we have different sections or pricing, we can adjust accordingly.

```sql
-- Inserting tickets for the event with available status
INSERT INTO Tickets (TicketID, EventID, Price, SeatNumber, TicketStatus) 
VALUES (1, 1, 100.00, 'A1', 'AVAILABLE'),
       (2, 1, 100.00, 'A2', 'AVAILABLE'),
       (3, 1, 100.00, 'A3', 'AVAILABLE');
```

---

### **4. Initial Booking State**  
At this point, there are no bookings yet, so the **Bookings** table will be empty until a user books a ticket.

---

This gives our system an initial state where:

- **Dodgers Stadium** is listed as the venue.
- **An event** is scheduled at this venue.
- **Tickets** are created and available for booking.


-----

# Create a booking

Here’s a complete guide to create a **booking for 6 tickets** in our system, assuming a venue capacity of 56,000:

---

### **Step 1: Query for Available Tickets**  
Select 6 available tickets for the specified event at Dodgers Stadium.

```sql
SELECT TicketID 
FROM Tickets 
WHERE EventID = 1 AND TicketStatus = 'AVAILABLE' 
LIMIT 6;
```

If the query returns fewer than 6 rows, notify the user that there aren’t enough available tickets.

---

### **Step 2: Start Transaction**  
Begin a transaction to ensure atomicity of the operations.

```sql
START TRANSACTION;
```

---

### **Step 3: Insert Booking Records for Each Ticket**  
For each ticket returned by the query, insert a new row in the **Bookings** table.

```sql
INSERT INTO Bookings (BookingID, UserID, TicketID, BookingDate, PaymentStatus) 
VALUES (1001, 123, 1, CURRENT_TIMESTAMP, 'PENDING'),
       (1002, 123, 2, CURRENT_TIMESTAMP, 'PENDING'),
       (1003, 123, 3, CURRENT_TIMESTAMP, 'PENDING'),
       (1004, 123, 4, CURRENT_TIMESTAMP, 'PENDING'),
       (1005, 123, 5, CURRENT_TIMESTAMP, 'PENDING'),
       (1006, 123, 6, CURRENT_TIMESTAMP, 'PENDING');
```

---

### **Step 4: Update Ticket Status to 'BOOKED'**  
Update the status of each booked ticket to prevent double bookings.

```sql
UPDATE Tickets 
SET TicketStatus = 'BOOKED' 
WHERE TicketID IN (1, 2, 3, 4, 5, 6);
```

---

### **Step 5: Commit the Transaction**  
Ensure that the booking operation completes successfully.

```sql
COMMIT;
```

---

### **Step 6: Handle Payment**  
After payment processing succeeds, update the payment status.

```sql
UPDATE Bookings 
SET PaymentStatus = 'COMPLETED' 
WHERE BookingID IN (1001, 1002, 1003, 1004, 1005, 1006);
```

---

This transactional approach ensures consistency and prevents double booking.


----

# Better booking experience: No need to transition from Reserved to Available

## Approach-1: 
### **Recommendation: Implicit Status with Expiration Time**  

#### **Approach**  
- Recognize that ticket status is defined by two attributes:  
  - **Available**  
  - **Reserved but expired**  
- Avoid long-running transactions or locks by using **short transactions** that update ticket fields with reservation status and expiration time.  
- Key steps in the transaction process:  
  - Begin a transaction.  
  - Check if the ticket is either **available** or **reserved but expired**.  
  - If valid, update the ticket status to `RESERVED` and set an expiration time (e.g., `now + 10 minutes`).  
  - Commit the transaction.  
- This ensures:  
  - Only one user can reserve or book a ticket.  
  - Expired reservations can be reclaimed without delays.

---

#### **Advantages**  
- Eliminates dependency on cron jobs for releasing expired reservations.  
- Allows users to reclaim tickets from expired reservations seamlessly.  
- Efficient and scalable due to short transactions.

---

#### **Challenges and Solutions**  
- **Slower Read Operations:**  
  - Reads must filter tickets by both status and expiration time.  
  - Solution: Utilize **materialized views** and a **compound index** on (`Status`, `ExpirationTime`).  
- **Data Legibility:**  
  - Expired reservations remain in the database until cleaned up.  
  - Solution: Periodic **optional cleanup jobs** (cron) to mark expired reservations as available.  
  - Crucially, system behavior remains unaffected if the cleanup is delayed.

---

This approach combines efficiency, fairness, and resilience, ensuring a scalable ticket reservation system.

---

### **Why This Works Well**
- **Implicit State with Expiration:** No need for cron jobs or separate cleanup processes to release stale reservations.  
- **Short Transactions:** Reduces contention and ensures scalability.  
- **Efficient Expiration Check:** The ticket is considered available again if the expiration has passed, even if a cleanup job hasn’t run.  
- **Concurrent Safety:** Transactions ensure atomic updates, preventing race conditions.

---

### **Recommended Database Schema for Ticket Table**
```sql
CREATE TABLE Tickets (
    TicketID INT PRIMARY KEY,
    EventID INT,
    Status ENUM('AVAILABLE', 'RESERVED'),
    ExpirationTime DATETIME DEFAULT NULL,
    UNIQUE(EventID, TicketID)
);
```

---

### **Steps for Reservation Process (Pseudocode)**

#### **1. Begin a Database Transaction**
```sql
BEGIN;
```

#### **2. Check Current Ticket Status**
```sql
SELECT Status, ExpirationTime
FROM Tickets
WHERE TicketID = ?
AND (Status = 'AVAILABLE' OR ExpirationTime < CURRENT_TIMESTAMP)
FOR UPDATE;
```
- The `FOR UPDATE` clause locks the row temporarily during the transaction.

#### **3. Update Reservation if Available or Expired**
```sql
UPDATE Tickets 
SET Status = 'RESERVED', 
    ExpirationTime = CURRENT_TIMESTAMP + INTERVAL 10 MINUTE
WHERE TicketID = ?;
```

#### **4. Commit the Transaction**
```sql
COMMIT;
```

---

### **Handling Expired Reservations**
- Simply filter expired tickets using `WHERE Status = 'RESERVED' AND ExpirationTime < CURRENT_TIMESTAMP`.  
- Periodic clean-up jobs (optional) can run without disrupting system behavior.  

---

### **Challenges and Solutions**

| **Challenge** | **Solution** |
|---------------|--------------|
| Slower Reads | Use **compound indexes** on (`Status`, `ExpirationTime`) for efficient filtering. |
| Data Legibility | Optional cleanup jobs to mark expired reservations as `AVAILABLE`. |
| Concurrency | Rely on short-lived transactions with `FOR UPDATE`. |

---

### **Why This is Better**
- **No Long Locks:** Operations are atomic and quick.  
- **No Cron Job Dependency:** System state remains correct even if periodic clean-up fails or is delayed.  
- **Fairness:** Users can claim expired reservations without waiting.  

This design ensures scalability and efficiency, especially in high-demand systems like yours with **only 56,000 seats for 10 million interested users**.

## Approach-2:

### **Recommendation: Distributed Lock with TTL**  

#### **Approach**  
- Use **Redis**, an in-memory data store, to implement a distributed lock with a **Time To Live (TTL)** for the ticket reservation process.  
- Key steps in the solution:  
  - When a user selects a ticket, the system acquires a lock in Redis using a unique identifier (such as the ticket ID) and sets a TTL.  
  - The TTL acts as an automatic expiration time for the lock.  
  - If the user successfully completes the purchase:  
    - The ticket's status is updated to `BOOKED` in the database.  
    - The lock in Redis is manually released.  
  - If the TTL expires (indicating the user didn't complete the purchase), Redis automatically releases the lock, making the ticket available again.  
- Simplified ticket status states in the database:  
  - `AVAILABLE`  
  - `BOOKED`  
- The lock ensures that only the user who reserved the ticket can complete the booking.

---

#### **Advantages**  
- **Automatic Lock Expiration:** No need for manual cleanup or cron jobs.  
- **Efficient Concurrency Handling:** Redis handles high-concurrency operations effectively.  
- **Fair Access:** Expired reservations are seamlessly released for other users.  
- **Lightweight Design:** The database only stores `AVAILABLE` and `BOOKED` states, with Redis managing reservation logic.

---

#### **Challenges and Solutions**  
- **Handling Failures:**  
  - If Redis goes down, there may be a period where ticket reservation fails.  
  - Solution: Use Redis with high availability configurations (e.g., Redis Cluster, replication).  
- **User Experience Degradation:**  
  - Users may encounter errors if Redis fails or another user books the ticket first.  
  - Solution: Use database concurrency control mechanisms (e.g., Optimistic Concurrency Control - OCC) to prevent double bookings.  
- **Error Handling Post-Payment:**  
  - Users might see an error if someone else completes the booking during payment.  
  - While inconvenient, this is better than the system blocking all tickets if cleanup jobs fail.  

This approach offers scalability, efficiency, and a seamless user experience while ensuring system resilience.

--- 

# Virtual wait queue

### **Recommendation: Virtual Waiting Queue System**  

#### **Approach**  
- **Queue Management:**  
  - Place users in a virtual queue when they attempt to access the booking page for high-demand events.  
  - A unique identifier (such as a WebSocket connection ID) is used to track each user.  

- **Real-Time Notifications:**  
  - Establish a **WebSocket connection** between the server and user for continuous updates.  
  - Notify users via WebSocket when it's their turn to access the ticket booking page.  

- **Controlled Flow:**  
  - Periodically dequeue users based on factors like ticket availability and system capacity.  
  - Grant access by updating the database to reflect that a specific user can now proceed to the ticket purchasing system.  

#### **Challenges & Solutions**
- **User Frustration:**  
  - Long queue wait times may cause dissatisfaction.  
  - Real-time updates on queue position and estimated wait times via WebSocket can reduce frustration.  

- **Accuracy of Wait Times:**  
  - Keep dynamic estimates of queue movement speed based on real-time factors like ticket bookings and user drop-offs.  

#### **Benefits**  
- Prevents system overload by controlling concurrent access to the booking system.  
- Enhances user experience with transparent communication during high-demand events.



# References:
1. https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster
2. https://bytebytego.com/courses/system-design-interview/hotel-reservation-system