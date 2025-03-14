import streamlit as st
import json
import os

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    """Load the library from a file."""
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    """Save the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    """Add a book to the library."""
    library.append({
        "Title": title,
        "Author": author,
        "Year": int(year),
        "Genre": genre,
        "Read": read_status
    })
    save_library(library)

def remove_book(library, title):
    """Remove a book by title."""
    updated_library = [book for book in library if book["Title"].lower() != title.lower()]
    if len(updated_library) < len(library):
        save_library(updated_library)
    return updated_library

def search_books(library, query):
    """Search for books by title or author."""
    return [book for book in library if query.lower() in book["Title"].lower() or query.lower() in book["Author"].lower()]

def get_statistics(library):
    """Get total books and percentage read."""
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

# Streamlit UI Configuration
st.set_page_config(page_title="📚 Book Haven", page_icon="📖", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        /* Light Pinkish Background */
        body, .main {
            background-color: #FCE4EC;
            color: #333;
        }

        /* Title Styling */
        .title-text {
            font-size: 2.5em;
            font-weight: bold;
            color: #D81B60;
            text-align: center;
        }

        /* Subtitle Styling */
        .subtitle-text {
            font-size: 1.2em;
            color: #6A1B9A;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Form Container */
        .form-container {
            background: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            width: 60%;
            margin: auto;
        }

        /* Buttons */
        .stButton>button {
            background-color: #F06292;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #D81B60;
        }

        /* Footer */
        .footer {
            text-align: center;
            font-size: 0.9em;
            color: #D81B60;
            margin-top: 50px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown("<h1 class='title-text'>📚 Welcome to Book Haven</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>\"A reader lives a thousand lives before he dies.\" - George R.R. Martin</p>", unsafe_allow_html=True)

library = load_library()

# Sidebar Menu
st.sidebar.title("📌 Library Menu")
menu = st.sidebar.radio("Choose an option", ["Add a Book", "Remove a Book", "Search Books", "View All Books", "Statistics"])

if menu == "Add a Book":
    st.subheader("📖 Add a New Book")
    with st.container():
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Mark as Read")

        if st.button("➕ Add Book"):
            if title and author and year and genre:
                add_book(library, title, author, year, genre, read_status)
                st.success(f"✅ '{title}' added to your library!")
            else:
                st.warning("⚠️ Please fill all fields.")

elif menu == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter the book title to remove")
    if st.button("❌ Remove Book"):
        library = remove_book(library, title)
        st.success(f"✅ '{title}' removed from your library.")

elif menu == "Search Books":
    st.subheader("🔍 Search for a Book")
    query = st.text_input("Search by title or author")
    if st.button("🔎 Search"):
        results = search_books(library, query)
        if results:
            for book in results:
                st.markdown(f"**📖 {book['Title']}** by *{book['Author']}* ({book['Year']}) - {'✅ Read' if book['Read'] else '❌ Unread'}")
        else:
            st.warning("⚠️ No matching books found.")

elif menu == "View All Books":
    st.subheader("📚 Your Book Collection")
    if library:
        for book in library:
            st.markdown(f"**📖 {book['Title']}** by *{book['Author']}* ({book['Year']}) - {'✅ Read' if book['Read'] else '❌ Unread'}")
    else:
        st.warning("⚠️ Your library is empty.")

elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books, percentage_read = get_statistics(library)
    st.write(f"📌 **Total Books:** {total_books}")
    st.write(f"📖 **Read Percentage:** {percentage_read:.2f}%")

# Footer
st.markdown("<div class='footer'>© 2025 Book Haven | Built with ❤️ by Ruba Haroon</div>", unsafe_allow_html=True)
