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
    """Create a new user in the Users table."""
    return curd.create_user(curd.CreateUser(name=name, mail=mail))


@mcp.tool()
def create_book(name: str, author_id: int, genre: str, desc: str):
    """Create a new book in the Books table."""
    return curd.create_book(
        curd.CreateBook(name=name, authorId=author_id, genre=genre, desc=desc, desc_vector="")
    )


@mcp.tool()
def create_author(name: str):
    """Create a new author in the Authors table."""
    return curd.create_author(curd.CreateAuthor(name=name))


@mcp.tool()
def create_slot(book_id: int, author_id: int):
    """Create a new slot in the Slots table."""
    return curd.create_slot(curd.CreateSlot(bookId=book_id, authorId=author_id))


@mcp.tool()
def update_user(id: int, name: Optional[str] = None, mail: Optional[str] = None):
    """Update an existing user."""
    return curd.update_user(id, UpdateUserPayload(name=name, mail=mail))


@mcp.tool()
def update_book(
    id: int,
    name: Optional[str] = None,
    author_id: Optional[int] = None,
    genre: Optional[str] = None,
    desc: Optional[str] = None,
):
    """Update an existing book."""
    return curd.update_book(
        id,
        UpdateBookPayload(name=name, authorId=author_id, genre=genre, desc=desc),
    )


@mcp.tool()
def update_author(id: int, name: Optional[str] = None):
    """Update an existing author."""
    return curd.update_author(id, UpdateAuthorPayload(name=name))


@mcp.tool()
def update_slot(id: int, book_id: Optional[int] = None, author_id: Optional[int] = None):
    """Update an existing slot."""
    return curd.update_slot(id, UpdateSlotPayload(bookId=book_id, authorId=author_id))


@mcp.tool()
def book_start_from(prefix: str):
    """Find books whose names start with the given text."""
    return curd.book_start_from(prefix)


@mcp.tool()
def book_end_with(suffix: str):
    """Find books whose names end with the given text."""
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
    """Fetch a book by its ID."""
    return curd.search_book(id)


@mcp.tool()
def search_author(id: int):
    """Fetch an author by their ID."""
    return curd.search_author(id)


@mcp.tool()
def search_user(id: int):
    """Fetch a user by their ID."""
    return curd.search_user(id)


@mcp.tool()
def search_book_isavail(id: int):
    """Check whether a slot exists for the given ID."""
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
    """Delete a user by ID."""
    return curd.delete_user(id)


@mcp.tool()
def delete_book(id: int):
    """Delete a book by ID."""
    return curd.delete_book(id)


@mcp.tool()
def delete_author(id: int):
    """Delete an author by ID."""
    return curd.delete_author(id)


@mcp.tool()
def delete_slot(id: int):
    """Delete a slot by ID."""
    return curd.delete_slot(id)


@mcp.tool()
def search_books_by_description(query_text: str, limit: int = 3):
    """Search books using description similarity."""
    return curd.search_books_by_description(query_text, limit)


if __name__ == "__main__":
    print("Server Started Nanbaa Chinna Saami")
    mcp.run()
