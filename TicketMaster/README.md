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

## ACID
### Atomicity: 
Abortability of a transaction. Either commit all queries in a transaction, or nothing.



## CAP theorem
1, 
