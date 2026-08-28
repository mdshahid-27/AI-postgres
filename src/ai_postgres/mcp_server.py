from typing import Optional

from mcp.server import FastMCP
from pydantic import BaseModel

from ai_postgres.tools import curd


mcp = FastMCP("AI Postgres")


class UpdateUserPayload(BaseModel):
    name: Optional[str] = None
    mail: Optional[str] = None


class UpdateBookPayload(BaseModel):
    name: Optional[str] = None
    authorId: Optional[int] = None
    genre: Optional[str] = None
    desc: Optional[str] = None


class UpdateAuthorPayload(BaseModel):
    name: Optional[str] = None


class UpdateSlotPayload(BaseModel):
    bookId: Optional[int] = None
    authorId: Optional[int] = None


@mcp.tool()
def create_user(name: str, mail: str):
    """Create a new user in the Users table.
    
    args : { 
    name : str | which is user name
    mail : mailaddress | which is user mail address
    }
    
    """
    return curd.create_user(curd.CreateUser(name=name, mail=mail))


@mcp.tool()
def create_book(name: str, author_id: int, genre: str, desc: str):
    """Create a new book in the Books table.
    args : {
    name : str | book name 
    author_id : int | Author id which present in author table
    genre : str | Book genre in text
    desc : str | Book's description
    }
    """
    return curd.create_book(
        curd.CreateBook(name=name, authorId=author_id, genre=genre, desc=desc, desc_vector="")
    )


@mcp.tool()
def create_author(name: str):
    """Create a new author in the Authors table.
    args : {
    name : str | Name for the new author
    }
    """
    return curd.create_author(curd.CreateAuthor(name=name))


@mcp.tool()
def create_slot(book_id: int, author_id: int):
    """Create a new slot in the Slots table.
    args : {
    book_id : int | id of the book which is booked
    author_is : int | id of the author which is booked
    }
    """
    return curd.create_slot(curd.CreateSlot(bookId=book_id, authorId=author_id))


@mcp.tool()
def update_user(id: int, name: Optional[str] = None, mail: Optional[str] = None):
    """Update an existing user.
    args : {
    id : int | user id for get user data from the able
    name : str | new name for the user  or None
    mail : str | new mail for the user  or None
    }
    """

    return curd.update_user(id, UpdateUserPayload(name=name, mail=mail))


@mcp.tool()
def update_book(
    id: int,
    name: Optional[str] = None,
    author_id: Optional[int] = None,
    genre: Optional[str] = None,
    desc: Optional[str] = None,
):
    """Update an existing book.
    args : {
    id : int | BookId to get book data
    name : str | new name for the book 
    author_id : str | new author id for the book
    genre : str | genre of the book
    desc : str | description about the book
    }
    """
    return curd.update_book(
        id,
        UpdateBookPayload(name=name, authorId=author_id, genre=genre, desc=desc),
    )


@mcp.tool()
def update_author(id: int, name: Optional[str] = None):
    """Update an existing author.
    args : {
    id : int | AuthorId to get data 
    name : str | new author name
    }
    """
    return curd.update_author(id, UpdateAuthorPayload(name=name))


@mcp.tool()
def update_slot(id: int, book_id: Optional[int] = None, author_id: Optional[int] = None):
    """Update an existing slot.
    args : {
    id : int | slotId to get slot data 
    book_id : int | new BookId to update 
    author_id : int | new author id to update
    }
    """
    return curd.update_slot(id, UpdateSlotPayload(bookId=book_id, authorId=author_id))


@mcp.tool()
def book_start_from(prefix: str):
    """Find books whose names start with the given text.
    args : {
    prefix : str | letter or letters start from
    }
    """
    return curd.book_start_from(prefix)


@mcp.tool()
def book_end_with(suffix: str):
    """Find books whose names end with the given text.
    args : {
    suffix : str | letter or letters end with
    }
    """
    return curd.book_end_with(suffix)


@mcp.tool()
def total_slots():
    """Count how many slots exist in the database."""
    return curd.total_slots()


@mcp.tool()
def view_genres():
    """Show the genres that exist in the database."""
    return curd.view_genres()


@mcp.tool()
def search_book(id: int):
    """Fetch a book by its ID.
    args : {
    id : int | id of the book in book table
    }
    """
    return curd.search_book(id)


@mcp.tool()
def search_author(id: int):
    """Fetch an author by their ID.
    args : {
    id : int | id of the author in author table
    }
    """
    return curd.search_author(id)


@mcp.tool()
def search_user(id: int):
    """Fetch a user by their ID.
    args : {
    id : int | id of the user from user table
    }
    """
    return curd.search_user(id)


@mcp.tool()
def search_book_isavail(id: int):
    """Check whether a slot exists for the given ID.
    args : {
    id : int | 
    }
    """
    return curd.search_book_isavail(id)


@mcp.tool()
def get_all_books():
    """Return every book in the database."""
    return curd.get_all_books()


@mcp.tool()
def get_all_users():
    """Return every user in the database."""
    return curd.get_all_users()


@mcp.tool()
def get_all_authors():
    """Return every author in the database."""
    return curd.get_all_authors()


@mcp.tool()
def get_all_slots():
    """Return every slot in the database."""
    return curd.get_all_slots()


@mcp.tool()
def delete_user(id: int):
    """Delete a user by ID.
    args : {
    id : int | id of the user to delete 
    }
    """
    return curd.delete_user(id)


@mcp.tool()
def delete_book(id: int):
    """Delete a book by ID.
    args : {
    id : int | id of the book to delete
    }
    """
    return curd.delete_book(id)


@mcp.tool()
def delete_author(id: int):
    """Delete an author by ID.
    args : {
    id : int | id of the author to delete
    }
    """
    return curd.delete_author(id)


@mcp.tool()
def delete_slot(id: int):
    """Delete a slot by ID.
    args : {
    id : int | id of the slot to delete
    }
    """
    return curd.delete_slot(id)


@mcp.tool()
def search_books_by_description(query_text: str, limit: int = 3):
    """Search books using description similarity.
    args : {
    query_text : str | description by user to find the book
    }
    """
    return curd.search_books_by_description(query_text, limit)


if __name__ == "__main__":
    print("Server Started Nanbaa Chinna Saami")
    mcp.run()
