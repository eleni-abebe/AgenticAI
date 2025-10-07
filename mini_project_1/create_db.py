import sqlite3

# Step 1: Connect to SQLite (creates student.db if it doesn't exist)
conn = sqlite3.connect("student.db")
cur = conn.cursor()

# Step 2: Create the STUDENT table
cur.execute("""
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(100),
    CLASS VARCHAR(50),
    SECTION VARCHAR(10),
    MARKS INT
)
""")

# Step 3: Insert some sample data
students = [
    ("Eleni Abebe", "Data Science", "A", 95),
    ("Abebe Tadesse", "AI", "B", 88),
    ("Sara Alem", "Data Science", "A", 92),
    ("Kebede Fikadu", "AI", "B", 85)
]

cur.executemany("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?)", students)

# Step 4: Save and close
conn.commit()
conn.close()

print("Database created and STUDENT table initialized successfully!")
