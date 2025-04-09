from fastapi import FastAPI, HTTPException # Core framework to build API, returns custom error responses - 404 Not Found
from pydantic import BaseModel # define data models (schemas) with validations

app = FastAPI() # Create an instance of FastAPI app
 
books = [] # In-memory "database", a list acting like a database

# Schema for book
class Book(BaseModel): # since it inherits from BaseModel, FastAPI will automatically valid input data and generate JSON schemas for docs
    id: int
    title: str
    author: str

@app.get("/") # Basic Root route that returns a welcome message
def read_root():
    return {"message": "Welcome to Book API"}

@app.get("/books") # Returns all books that are currently in the books list
def get_books():
    return books

@app.get("/books/{book_id}") # Loops through the books list to find a book with a given id, if found return it, if not raise 404 Not Found error
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books") # Takes a Book object from the request body, Appends it to the books list and return book data as a response
def create_book(book: Book):
    books.append(book)
    return book

@app.put("/books/{book_id}") # Searches for a book by id. If found, replaces it with updated_book. If not, returns a 404 error.
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}") # Searches for a book by id. Deletes it if found. Returns a simple confirmation message. If not found, throws a 404 error.
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            del books[index]
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
