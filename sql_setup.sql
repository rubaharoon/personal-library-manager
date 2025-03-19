-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Create Books Table
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL,
    genre TEXT NOT NULL,
    read_status TEXT NOT NULL DEFAULT 'Unread',
    cover_path TEXT,
    rating INTEGER DEFAULT 3 CHECK (rating BETWEEN 1 AND 5)
);

-- Create Issued Books Table
CREATE TABLE IF NOT EXISTS issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    issued_to TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

-- Insert Default Admin User
INSERT INTO users (username, password)
SELECT 'admin', 'e807f1fcf82d132f9bb018ca6738a19f55c19ad5f82a4c4e5cdbf03c03be7a5a'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');

-- Insert Sample Books
INSERT INTO books (title, author, year, genre, read_status, cover_path, rating)
SELECT 'The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Fiction', 'Read', 'gatsby.jpeg', 5
WHERE NOT EXISTS (SELECT 1 FROM books);

INSERT INTO books (title, author, year, genre, read_status, cover_path, rating)
SELECT 'To Kill a Mockingbird', 'Harper Lee', 1960, 'Classic', 'Read', 'mocking-bird.jpeg', 5
WHERE NOT EXISTS (SELECT 1 FROM books);

INSERT INTO books (title, author, year, genre, read_status, cover_path, rating)
SELECT '1984', 'George Orwell', 1949, 'Dystopian', 'Unread', '1984.jpeg', 4
WHERE NOT EXISTS (SELECT 1 FROM books);

INSERT INTO books (title, author, year, genre, read_status, cover_path, rating)
SELECT 'Pride and Prejudice', 'Jane Austen', 1813, 'Romance', 'Read', 'prideandprejudice.jpeg', 5
WHERE NOT EXISTS (SELECT 1 FROM books);

INSERT INTO books (title, author, year, genre, read_status, cover_path, rating)
SELECT 'The Hobbit', 'J.R.R. Tolkien', 1937, 'Fantasy', 'Unread', 'hobbit.jpeg', 4
WHERE NOT EXISTS (SELECT 1 FROM books);
