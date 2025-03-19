import sqlite3
import hashlib

# Connect to SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create Users Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

# Create Books Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        genre TEXT NOT NULL,
        read_status TEXT NOT NULL DEFAULT 'Unread',
        cover_path TEXT,
        rating INTEGER DEFAULT 3 CHECK (rating BETWEEN 1 AND 5)
    )
""")

# Create Issued Books Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS issued_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        issued_to TEXT NOT NULL,
        issue_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
    )
""")

# Hash the default admin password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Insert Default Admin User (if not exists)
cursor.execute("SELECT 1 FROM users WHERE username = ?", ('admin',))
if cursor.fetchone() is None:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   ('admin', hash_password('12345678')))

# Insert Sample Books (with Cover Paths & Ratings)
sample_books = [
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction", "Read", "gatsby.jpeg", 5),
    ("To Kill a Mockingbird", "Harper Lee", 1960, "Classic", "Read", "mocking-bird.jpeg", 5),
    ("1984", "George Orwell", 1949, "Dystopian", "Unread", "1984.jpeg", 4),
    ("Pride and Prejudice", "Jane Austen", 1813, "Romance", "Read", "prideandprejudice.jpeg", 5),
    ("The Hobbit", "J.R.R. Tolkien", 1937, "Fantasy", "Unread", "hobbit.jpeg", 4),
]

cursor.execute("SELECT COUNT(*) FROM books")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO books (title, author, year, genre, read_status, cover_path, rating) VALUES (?, ?, ?, ?, ?, ?, ?)", 
        sample_books
    )

# Commit Changes & Close Connection
conn.commit()
conn.close()

print("Database setup completed successfully!")
