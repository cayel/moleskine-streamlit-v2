# This Python file defines a Book class with methods for initialization, string representation, and a function to save book instances to a SQLite database.

class Book:
    def __init__(self, title, author, ISBN):
        # Initialize a new Book instance with title, author, and ISBN
        self.title = title
        self.author = author
        self.ISBN = ISBN

    def __str__(self):
        # Return a string representation of the Book instance
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.ISBN}"

    def __repr__(self):
        # Return an unambiguous string representation of the Book instance
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.ISBN}"

class BookList:
    def __init__(self):
        # Initialize a new BookList instance with an empty list of books
        self.books = []

    def add_book(self, book):
        # Add a Book instance to the list of books
        self.books.append(book)
        
    def __str__(self):
        # Return a string representation of the BookList instance, which is a list of string representations of the Book instances
        return "\n".join([str(book) for book in self.books])

    def __repr__(self):
        # Return an unambiguous string representation of the BookList instance, which is a list of unambiguous string representations of the Book instances
        return "\n".join([repr(book) for book in self.books])
    
    # Sort the books by title in ascending order
    def sort_books_by_title(self):
        self.books.sort(key=lambda x: x.title)
        
def save_book_to_db(book):
    # Save a Book instance to the 'books' table in the 'test.db' SQLite database
    import sqlite3
    conn = sqlite3.connect('test.db')  # Connect to the SQLite database
    c = conn.cursor()
    # Create the 'books' table if it does not exist
    c.execute("CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, ISBN TEXT)")
    # Insert the Book instance into the 'books' table
    c.execute("INSERT INTO books (title, author, ISBN) VALUES (?, ?, ?)", (book.title, book.author, book.ISBN))
    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection

