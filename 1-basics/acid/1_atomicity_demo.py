import sqlite3

# Connect to the SQLite database
with sqlite3.connect('example.db') as conn:
    cursor = conn.cursor()

    try:
        # Begin a transaction
        conn.execute("BEGIN")

        # Execute some SQL commands within the transaction
        cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
        cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")

        # Commit the transaction
        conn.commit()
        print("Transaction committed successfully.")

    except sqlite3.Error as e:
        # Rollback the transaction in case of error
        conn.rollback()
        print(f"An error occurred: {e}. Transaction rolled back.")