import requests

def get_book_info(isbn):
    """
    Retrieve book information from Google Books API using an ISBN number.
    
    This function sends a request to the Google Books API and extracts information
    about the book corresponding to the given ISBN number. It specifically extracts
    the title and the first author of the book from the API's response.
    
    Parameters:
    - isbn (str): The ISBN number of the book for which information is being retrieved.
    
    Returns:
    - dict: A dictionary containing the title and the first author of the book.
            If the book is not found, returns a dictionary with "Title not found"
            and "Author not found" as placeholders. If the API call fails or the
            response is not as expected, returns None.
    
    Raises:
    - requests.exceptions.RequestException: An error occurred while making the request to the Google Books API.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        data = response.json()
        
        if data["totalItems"] > 0:
            book_data = data["items"][0]["volumeInfo"]
            return {
                "title": book_data.get("title", "Title not found"),
                "authors": book_data.get("authors", ["Author not found"])[0]
            }
        else:
            return {"title": "Title not found", "authors": "Author not found"}
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_book_info_from_title_author(title, author):
    """
    Retrieve book information from Google Books API using the title and author.
    
    This function sends a request to the Google Books API and extracts information
    about the book corresponding to the given title and author. It specifically extracts
    the ISBN number of the book from the API's response.
    
    Parameters:
    - title (str): The title of the book for which information is being retrieved.
    - author (str): The author of the book for which information is being retrieved.
    
    Returns:
    - dict: A dictionary containing the ISBN number of the book.
            If the book is not found, returns a dictionary with "ISBN not found" as a placeholder.
            If the API call fails or the response is not as expected, returns None.
    
    Raises:
    - requests.exceptions.RequestException: An error occurred while making the request to the Google Books API.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}+inauthor:{author}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        data = response.json()
        
        if data["totalItems"] > 0:
            book_data = data["items"][0]["volumeInfo"]
            print(book_data)
            return {
                "isbn": book_data.get("industryIdentifiers", [{"type": "ISBN_13", "identifier": "ISBN not found"}])[0]["identifier"],
                "title": book_data.get("title", "Title not found")
            }
        else:
            return {"isbn": "ISBN not found"}
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def get_book_image(isbn):
    """
    Retrieve book cover image from Google Books API using an ISBN number.
    
    This function sends a request to the Google Books API and extracts the link
    to the book cover image corresponding to the given ISBN number.
    
    Parameters:
    - isbn (str): The ISBN number of the book for which the cover image is being retrieved.
    
    Returns:
    - str: A URL link to the book cover image.
            If the image is not found, returns a placeholder image link.
            If the API call fails or the response is not as expected, returns None.
    
    Raises:
    - requests.exceptions.RequestException: An error occurred while making the request to the Google Books API.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        data = response.json()
        
        if data["totalItems"] > 0:
            book_data = data["items"][0]["volumeInfo"]
            return book_data.get("imageLinks", {"thumbnail": "Image not found"})["thumbnail"]
        else:
            return "Image not found"
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
# Search a book from a string input
def search_books(search_string):
    """
    Search for books using a search string.
    
    This function sends a request to the Google Books API and extracts information
    about the books corresponding to the given search string. It specifically extracts
    the title, authors, and ISBN numbers of the books from the API's response.
    
    Parameters:
    - search_string (str): The search string used to find books.
    
    Returns:
    - list: A list of dictionaries, where each dictionary contains the title, authors,
            and ISBN number of a book. If no books are found, returns an empty list.
            If the API call fails or the response is not as expected, returns None.
    
    Raises:
    - requests.exceptions.RequestException: An error occurred while making the request to the Google Books API.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q={search_string}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        data = response.json()
        
        books = []
        if data["totalItems"] > 0:
            for item in data["items"]:
                book_data = item["volumeInfo"]
                isbn = book_data.get("industryIdentifiers", [{"type": "ISBN_13", "identifier": "ISBN not found"}])[0]["identifier"]
                title = book_data.get("title", "Title not found")
                authors = book_data.get("authors", ["Author not found"])
                books.append({"title": title, "authors": authors, "isbn": isbn})                
            return books
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None