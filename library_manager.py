import os
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database setup
DB_PATH = "library.db"
if not os.path.exists(DB_PATH):
    st.error("Database not found. Please run `sqlite_setup.py` first.")
    st.stop()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Streamlit setup
st.set_page_config(page_title="Book Haven 📚", layout="wide")

st.markdown(
    """
    <style>
        .main { background-color: #ffe6f2; }
        .title-text { text-align: center; font-size: 24px; font-weight: bold; }
        .quote { color: purple; text-align: center; font-style: italic; font-size: 18px; }
        
        /* Footer Styling */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: gray;
            z-index: 100;
        }
    </style>
    <div class="footer">📚 Book Haven | Made with ❤️ by Ruba Haroon</div>
    """,
    unsafe_allow_html=True
)


# Login Page
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("<h1 class='title-text'>📖 Welcome to Book Haven</h1>", unsafe_allow_html=True)
    st.markdown("<p class='quote'>\"A reader lives a thousand lives before he dies.\"</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        image = Image.open("libraryimage.jpeg")
        st.image(image, use_container_width=True)
    with col2:
        st.markdown("<h2>🔑 Login to Access Book Haven</h2>", unsafe_allow_html=True)
        name = st.text_input("👤 Name")
        email = st.text_input("✉️ Login with Email")
        if st.button("Login"):
            if email:
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                st.rerun()
    st.stop()

# Sidebar Menu
st.sidebar.title(f"👋 Welcome, {st.session_state['email']}")
menu_choice = st.sidebar.radio("📚 Menu", [
    "📖 View All Books", "📚 Add Book", "🔍 Search Book",
    "🗑 Delete Book", "📙 Issue Book", "📕 Return Book",
    "📊 Statistics", "📥 Import/Export Data", "🔴 Logout"
])

if menu_choice == "📖 View All Books":
    st.header("📖 View All Books")
    conn = get_db_connection()
    search_query = st.text_input("🔍 Search by Title, Author, or Genre")
    show_available_only = st.checkbox("📗 Show Only Available Books")

    query = "SELECT * FROM books"
    params = []
    if search_query:
        query += " WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?"
        params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
    if show_available_only:
        query += " AND id NOT IN (SELECT book_id FROM issued_books)" if "WHERE" in query else " WHERE id NOT IN (SELECT book_id FROM issued_books)"

    books = conn.execute(query, params).fetchall()
    conn.close()
    
    for book in books:
        st.markdown(f"**📖 {book['title']}** by {book['author']} ({book['year']})")
        if book["cover_path"]:
            st.image(book["cover_path"], width=100)

elif menu_choice == "📚 Add Book":
    st.header("📚 Add a New Book")

    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100)

    # File uploader for book cover
    book_cover = st.file_uploader("📸 Upload Book Cover", type=["jpg", "jpeg", "png"])

    # Initialize cover_path
    cover_path = ""

    # Handle file upload properly
    if book_cover is not None:
        cover_path = os.path.join(UPLOAD_FOLDER, book_cover.name)
        with open(cover_path, "wb") as f:
            f.write(book_cover.getbuffer())

    reading_status = st.selectbox("Reading Status", ["Reading", "Read", "Unread"])
    rating = st.slider("Rating", 1, 5, 3)

    if st.button("➕ Add Book"):
        if not title or not author or not genre or not year:
            st.error("⚠️ Please fill in all the required fields.")
        else:
            with get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO books (title, author, genre, year, cover_path, read_status, rating) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (title, author, genre, year, cover_path, reading_status, rating)
                )
                conn.commit()
                st.success("✅ Book added successfully!")
    
elif menu_choice == "🔍 Search Book":
        st.header("🔍 Search Books")
        search_query = st.text_input("Enter book title or author")
        if search_query:
            conn = get_db_connection()
            books = conn.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{search_query}%", f"%{search_query}%")).fetchall()
            conn.close()
            for book in books:
                st.markdown(f"**📖 {book['title']}** by {book['author']} ({book['year']})")
    
elif menu_choice == "🗑 Delete Book":
        st.header("🗑 Delete Book")
        conn = get_db_connection()
        books = conn.execute("SELECT id, title FROM books").fetchall()
        book_to_delete = st.selectbox("Select a book to delete", [book["title"] for book in books])
        if st.button("🗑 Delete Book"):
            with conn:
                conn.execute("DELETE FROM books WHERE title = ?", (book_to_delete,))
                conn.commit()
                st.success("✅ Book deleted successfully!")
    
elif menu_choice == "📙 Issue Book":
        st.header("📙 Issue a Book")
        conn = get_db_connection()
        books = conn.execute("SELECT id, title FROM books").fetchall()
        book_id = st.selectbox("Select Book", [book["title"] for book in books])
        issued_to = st.text_input("Issued to (Name)")
        issue_date = st.date_input("Issue Date")
        due_date = st.date_input("Due Date")
        if st.button("📙 Issue Book"):
            with conn:
                conn.execute("INSERT INTO issued_books (book_id, issued_to, issue_date, due_date) VALUES ((SELECT id FROM books WHERE title = ?), ?, ?, ?)",
                             (book_id, issued_to, issue_date, due_date))
                conn.commit()
                st.success("✅ Book issued successfully!")
    
elif menu_choice == "📕 Return Book":
        st.header("📕 Return a Book")
        conn = get_db_connection()
        issued_books = conn.execute("SELECT id, book_id, issued_to FROM issued_books").fetchall()
        if issued_books:
            book_to_return = st.selectbox("Select Issued Book", [f"{book['issued_to']} - {book['book_id']}" for book in issued_books])
            if st.button("📕 Return Book"):
                with conn:
                    conn.execute("DELETE FROM issued_books WHERE book_id = ?", (book_to_return.split(" - ")[1],))
                    conn.commit()
                    st.success("✅ Book returned successfully!")
        else:
            st.info("📭 No books are currently issued.")
    
elif menu_choice == "📊 Statistics":
        st.header("📊 Library Statistics")
        conn = get_db_connection()
        
        # Fetch data
        total_books = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        issued_books = conn.execute("SELECT COUNT(*) FROM issued_books").fetchone()[0]
        available_books = total_books - issued_books
    
        reading_status_counts = conn.execute(
            "SELECT read_status, COUNT(*) FROM books GROUP BY read_status"
        ).fetchall()
    
        top_genres = conn.execute(
            "SELECT genre, COUNT(*) as count FROM books GROUP BY genre ORDER BY count DESC LIMIT 5"
        ).fetchall()
    
        ratings = conn.execute("SELECT rating FROM books").fetchall()
        conn.close()
    
        # Quick Overview
        col1, col2, col3 = st.columns(3)
        col1.metric("📚 Total Books", total_books)
        col2.metric("📕 Issued Books", issued_books)
        col3.metric("📖 Available Books", available_books)
    
        # Reading Status Pie Chart
        st.subheader("📖 Reading Status Distribution")
        if reading_status_counts:
            labels, values = zip(*reading_status_counts)
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
            st.pyplot(fig)
        else:
            st.info("No reading status data available.")
    
        # Reading Progress (Bar Chart)
        st.subheader("📊 Reading Progress")
        if reading_status_counts:
            fig, ax = plt.subplots()
            ax.bar(labels, values, color=['#ff9999','#66b3ff','#99ff99'])
            ax.set_ylabel("Number of Books")
            st.pyplot(fig)
        else:
            st.info("No reading progress data available.")
    
        # Top Genres (Bar Chart)
        st.subheader("🎭 Top 5 Genres")
        if top_genres:
            genres, counts = zip(*top_genres)
            fig, ax = plt.subplots()
            ax.barh(genres, counts, color='#ffcc99')
            ax.set_xlabel("Number of Books")
            st.pyplot(fig)
        else:
            st.info("No genre data available.")
    
        # Rating Distribution (Histogram)
        st.subheader("⭐ Rating Distribution")
        if ratings:
            rating_values = [r["rating"] for r in ratings]
            fig, ax = plt.subplots()
            ax.hist(rating_values, bins=5, range=(1, 5), color='#ffcc00', edgecolor='black')
            ax.set_xlabel("Rating (1-5)")
            ax.set_ylabel("Number of Books")
            st.pyplot(fig)
        else:
            st.info("No rating data available.")

elif menu_choice == "📥 Import/Export Data":
        st.header("📥 Import & Export Data")
        if st.button("📤 Export Data"):
            conn = get_db_connection()
            df = pd.read_sql_query("SELECT * FROM books", conn)
            conn.close()
            df.to_csv("exported_books.csv", index=False)
            st.success("📁 Data exported as 'exported_books.csv'")
    
        uploaded_file = st.file_uploader("📥 Upload CSV to Import Books", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            with get_db_connection() as conn:
                df.to_sql("books", conn, if_exists="append", index=False)
                conn.commit()
                st.success("✅ Books imported successfully!")
    
elif menu_choice == "🔴 Logout":
        st.session_state.clear()
        st.rerun()

st.markdown("<p class='footer'>📚 Book Haven | Made with ❤️ by Ruba Haroon</p>", unsafe_allow_html=True)
