import streamlit as st
import requests
from google_books_api import get_book_info
from google_books_api import get_book_info_from_title_author
from google_books_api import get_book_image
from google_books_api import search_books   

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

# Ajoute un bouton avec un emoji loupe pour la recherche du livre
search = st.button("Search 🔍")

# When I click on the submit button retrive books information from the Google Books API int the secon column
with col2:
    st.header("Book Cover Image")
    if search or st.session_state.search is not None:
        st.session_state.search = "search"
        results = search_books(search_string)
        if results is None:
            print("Failed to fetch data from Google Books API.")
        elif len(results) == 0:
            print("No books found for the given search string.")
        else:
            # Build a list of book titles with authors and number of each item
            # Supposons que `results` est une liste de dictionnaires avec les clés 'title' et 'authors'
            book_list = []
            for book in results:
                book_list.append(f"{book['title']} by {', '.join(book['authors'])}")

            # Numéroter les éléments de la liste
            book_list = [f"{i+1}. {book}" for i, book in enumerate(book_list)]

            # Convertir la liste en une chaîne de caractères pour l'affichage
            book_list_str = "\n".join(book_list)

            # Afficher la liste des livres
            st.text(book_list_str)
            # Select a book from the list
            selected_book = st.selectbox("Select a book:", book_list, index=0)
            book_index = int(selected_book.split(".")[0]) - 1
            book = results[book_index]
            # Get the book information
            book_info = get_book_info_from_title_author(book["title"], book["authors"])
            if book_info is None:
                print("Failed to fetch data from Google Books API.")
            else:
                st.write(book_info)
                # Get the book image
                book_image = get_book_image(book_info["isbn"])
                if book_image is None:
                    print("Failed to fetch data from Google Books API.")
                else:
                    st.image(book_image, caption=book_info["title"], use_column_width=False)
    else:
        st.write("Please click the search button to fetch book information.")



        
    

