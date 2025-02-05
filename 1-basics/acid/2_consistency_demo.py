import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create a table with a consistency rule: age must be positive
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER CHECK (age > 0) -- Consistency rule: age must be positive
)
''')
conn.commit()

def insert_user(name, age):
    try:
        # Begin a transaction
        conn.execute("BEGIN")

        # Insert a new user
        cursor.execute("INSERT INTO employees (name, age) VALUES (?, ?)", (name, age))

        # Commit the transaction
        conn.commit()
        print(f"User '{name}' with age {age} inserted successfully.")

    except sqlite3.IntegrityError as e:
        # Rollback the transaction if the consistency rule is violated
        conn.rollback()
        print(f"Failed to insert user '{name}': {e}. Transaction rolled back.")

    except sqlite3.Error as e:
        # Rollback for any other database errors
        conn.rollback()
        print(f"An error occurred: {e}. Transaction rolled back.")

# Test cases
insert_user("Alice", 30)  # Valid: age is positive
insert_user("Bob", -5)    # Invalid: age is negative (violates consistency rule)
insert_user("Charlie", 25) # Valid: age is positive

# Query the table to verify consistency
print("\nCurrent employees in the database:")
cursor.execute("SELECT * FROM employees")
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()
