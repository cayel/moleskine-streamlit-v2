import streamlit as st
import requests
from google_books_api import (
    get_book_info,
    get_book_info_from_title_author,
    get_book_info_from_title_author_isbn,
    get_book_image,
    search_books,
)
from book import Book, save_book_to_db
from datetime import date as Date

def initialize_session_state():
    if "search" not in st.session_state:
        st.session_state.search = None

def search_books_and_display():
    results = get_book_info_from_title_author_isbn(title, author, ISBN)
    if results is None:
        st.error("Failed to fetch data from Google Books API.")
    elif len(results) == 0:
        st.error("No books found for the given search string.")
    else:
        display_book_selection(results)

def display_book_selection(results):
    book_titles = [book["title"] for book in results]
    selected_book = st.selectbox("Select a book:", book_titles)
    selected_book_index = book_titles.index(selected_book)
    selected_book_info = results[selected_book_index]
    st.write(selected_book_info)
    display_book_image(selected_book_info)

def display_book_image(book_info):
    image_url = get_book_image(book_info["isbn"])
    if image_url is None:
        st.error("Failed to fetch image from Google Books API.")
    else:
        st.image(image_url, caption=book_info["title"], use_column_width=False)

def save_book(book_info):
    book = Book(book_info["title"], book_info["authors"][0], book_info["isbn"])
    save_book_to_db(book)
    st.success(f"The book {book.title} has been saved")

# Set Page Configuration
st.set_page_config(layout="wide")
initialize_session_state()

st.title("Welcome to Streamlit")
col1, col2 = st.columns([2, 3])

with col1:
    st.header("Book Information")
    search_string = st.text_input("Enter the search string:")
    author = st.text_input("Enter the author:")
    title = st.text_input("Enter the title:")
    ISBN = st.text_input("Enter the ISBN:")
    search = st.button("Search 🔍")
    save = st.button("Save 📚")

with col2:
    st.header("Book Cover Image")
    if search or st.session_state.search is not None:
        st.session_state.search = "search"
        search_books_and_display()
    if save:
        save_book(selected_book_info)