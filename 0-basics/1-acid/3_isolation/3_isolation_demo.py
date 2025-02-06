import sqlite3
import threading
import time
import uuid


def transaction_1(connection):
    cursor = connection.cursor()

    # Start Transaction 1
    cursor.execute("BEGIN TRANSACTION;")
    print("Transaction 1: Started")

    # Insert a user (this will be seen by Transaction 2 if 3_isolation is low)
    cursor.execute("INSERT INTO ISOLATION_USERS (id, name) VALUES (?, ?)", ("1", "Alice"))
    print("Transaction 1: Inserted User 'Alice'")

    time.sleep(3)  # Simulate a delay

    # Commit Transaction 1
    connection.commit()
    print("Transaction 1: Committed")


def transaction_2(connection):
    cursor = connection.cursor()

    # Start Transaction 2
    # cursor.execute("BEGIN TRANSACTION;")
    print("Transaction 2: Started")

    # Try to read data while Transaction 1 is not committed
    cursor.execute("SELECT * FROM ISOLATION_USERS WHERE id = ?", ("1",))
    result = cursor.fetchall()
    if result:
        print("Transaction 2: Found user:", result)
    else:
        print("Transaction 2: User not found")

    time.sleep(1)  # Simulate a short delay

    # Commit Transaction 2
    connection.commit()
    print("Transaction 2: Committed")


def main():
    # Create a shared connection for both threads
    connection = sqlite3.connect('../example.db', check_same_thread=False)
    connection.isolation_level = 'IMMEDIATE'
    print(f"Isolation level is {connection.isolation_level}")

    # Create ISOLATION_USERS table if not exists
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ISOLATION_USERS (
            id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(20)
        )
    """)
    connection.commit()

    # Start two threads to simulate concurrent transactions
    thread1 = threading.Thread(target=transaction_1, args=(connection,))
    thread2 = threading.Thread(target=transaction_2, args=(connection,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    cursor.execute("""
            DROP TABLE ISOLATION_USERS 
        """)

    # Close connection
    connection.close()


if __name__ == "__main__":
    main()


"""
Isolation level is DEFERRED - 
    Isolation level is 
    Transaction 1: Started
    Transaction 2: Started
    Transaction 1: Inserted User 'Alice'
    Transaction 2: Found user: [('1', 'Alice')]
    Transaction 2: Committed
    Transaction 1: Committed

-- Serializable
Output-1: 
    Isolation level is IMMEDIATE
    Transaction 1: Started
    Transaction 2: Started
    Transaction 2: User not found
    Transaction 1: Inserted User 'Alice'
    Transaction 2: Committed
    Transaction 1: Committed
    
Output-2:
    Isolation level is IMMEDIATE
    Transaction 1: Started
    Transaction 2: Started
    Transaction 1: Inserted User 'Alice'
    Transaction 2: Found user: [('1', 'Alice')]
    Transaction 2: Committed
    Transaction 1: Committed
"""
