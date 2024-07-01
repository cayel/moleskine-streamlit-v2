import streamlit as st
import requests
from google_books_api import get_book_info
from google_books_api import get_book_info_from_title_author
from google_books_api import get_book_image
from google_books_api import search_books   

# Set Page Configuration
st.set_page_config(layout="wide")

# Add a title
st.title("Welcome to Streamlit")

# Create two columns for the form and the image
col1, col2 = st.columns([2, 3])

# Add a form to entry the title and the writer of a book in the first column
with col1:
    st.header("Book Information")
    title = st.text_input("Enter the title of the book:")
    writer = st.text_input("Enter the writer of the book:")
    search_string = st.text_input("Enter the search string:")

# Ajoute un bouton avec un emoji loupe pour la recherche du livre
search = st.button("Search 🔍")

# When I click on the submit button retrive books information from the Google Books API int the secon column
with col2:
    st.header("Book Cover Image")
    if search:
        results = search_books(search_string)
        if results is None:
            print("Failed to fetch data from Google Books API.")
        elif len(results) == 0:
            print("No books found for the given search string.")
        else:
            for i, book in enumerate(results, start=1):
                st.text(f"Book {i}:")
                st.text(f"Title: {book['title']}")
                st.text(f"Authors: {', '.join(book['authors'])}")
                st.text(f"ISBN: {book['isbn']}\n")
                # Display image using Streamlit's image function
                image_url = get_book_image(book["isbn"])
                if image_url is not None:
                    st.image(image_url, caption="Book Cover")

        
        
    

