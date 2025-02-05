import sqlite3

# Connect to the database (it creates a new one if it doesn't exist)
connection = sqlite3.connect('example.db')
cursor = connection.cursor()

# Create a table
try:
    cursor.execute("""
        CREATE TABLE USERS (
            id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(20)
        )
    """)
except:
    print("The table already exists")

# Insert
cursor.executemany("""
    INSERT INTO USERS (id, name)
    VALUES (?, ?)
""", [
    ("1", "Alice"),
    ("2", "Bob"),
    ("3", "Charlie"),
    ("4", "David"),
    ("5", "Eva"),
    ("6", "Frank"),
    ("7", "Grace"),
    ("8", "Helen"),
    ("9", "Igor"),
    ("10", "Jack")
])

# Select
cursor.execute("SELECT * FROM users")
result = cursor.fetchall()
print(result)

# Close the connection
connection.close()
