import sqlite3
import os

DB_FILE = "example.db"


def setup_database():
    # Step 1: Connect to the database and create a table if it doesn't exist
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Create USERS table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    """)
    connection.commit()
    connection.close()
    print("Database setup complete.")


def insert_user(name):
    # Step 2: Insert a user and commit the transaction
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO USERS (name) VALUES (?)", (name,))
    connection.commit()  # Ensures changes are durable
    print(f"User '{name}' inserted and committed.")

    connection.close()


def verify_data():
    # Step 3: Verify data after reconnecting to the database
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM USERS")
    rows = cursor.fetchall()

    print("Data in USERS table after reconnecting:")
    for row in rows:
        print(row)

    connection.close()


if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)  # Start fresh to see durability clearly

    setup_database()
    insert_user("Alice")

    # Simulate program crash by ending script execution
    print("\nSimulating program crash...\n")

    # Step 4: Verify durability after "crash"
    verify_data()
