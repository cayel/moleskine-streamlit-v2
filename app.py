import streamlit as st
import requests
from google_books_api import get_book_info
from google_books_api import get_book_info_from_title_author
from google_books_api import get_book_info_from_title_author_isbn
from google_books_api import get_book_image
from google_books_api import search_books   
from book import Book
from book import save_book_to_db
from datetime import date as Date

# Set Page Configuration
st.set_page_config(layout="wide")

if "search" not in st.session_state:
    st.session_state.search = None

# Add a title
st.title("Welcome to Streamlit")

# Create two columns for the form and the image
col1, col2 = st.columns([2, 3])

# Add a form to entry the title and the writer of a book in the first column
with col1:
    st.header("Book Information")
    search_string = st.text_input("Enter the search string:")
    author = st.text_input("Enter the author:")
    title = st.text_input("Enter the title:")
    ISBN = st.text_input("Enter the ISBN:")

# Ajoute un bouton avec un emoji loupe pour la recherche du livre
search = st.button("Search 🔍")
# Ajoute un bouton enregistrement avec un emoji pour enregistrer le livre
save = st.button("Save 📚")

# When I click on the submit button retrive books information from the Google Books API int the secon column
with col2:
    st.header("Book Cover Image")
    if search or st.session_state.search is not None:
        st.session_state.search = "search"
        results = get_book_info_from_title_author_isbn(title, author, ISBN)
        if results is None:
            print("Failed to fetch data from Google Books API.")
        elif len(results) == 0:
            print("No books found for the given search string.")
        else:
            # build select box for the books found
            book_titles = [book["title"] for book in results]
            selected_book = st.selectbox("Select a book:", book_titles)
            selected_book_index = book_titles.index(selected_book)
            selected_book_info = results[selected_book_index]
            st.write(selected_book_info)
            # display image when a book is selected
            image_url = get_book_image(selected_book_info["isbn"])
            if image_url is None:
                st.write("Failed to fetch image from Google Books API.")
            else:
                print("===================================== Image URL =====================================")
                print(image_url)
                st.image(image_url, caption=selected_book_info["title"], use_column_width=False)
            book = Book(selected_book_info["title"], selected_book_info["authors"][0], selected_book_info["isbn"])            
            # Si je clique sur le bouton Save alors j'affiche une boite de dialoge avec le titre du livre
            if save:
                st.write(f"The book {book.title} has been saved")
                save_book_to_db(book)
