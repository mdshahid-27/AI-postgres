from sqlmodel import Session, create_engine, select, join, SQLModel, func
from ..schema.database import CreateBook, CreateAuthor, CreateSlot, CreateUser, UpdateAuthor,UpdateSlot, UpdateBook, UpdateUser, Users, Books, Authors, Slots

DATABASE_URL = "postgresql://postgres:postgres@localhost:5431/libray_ai"

engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

def create_user(data : CreateUser):
    '''This Tool for create user in User Table'''
    with Session(engine) as session:
        created = Users(
            name=data.name,
            mail = data.mail
        )
        session.add(created)
        session.commit()
        session.refresh(created)

        return 'Created Successfully'

def create_book(data: CreateBook):
    '''This tool is for create book in Books Table'''
    with Session(engine) as session:
        created = Books(
            name=data.name,
            author_id=data.authorId,
            genre=data.genre
        )
        session.add(created)
        session.commit()
        session.refresh(created)

        return 'Created Successfully'

def create_author(data : CreateAuthor):
    '''This tool is for create Author in Authors table'''
    with Session(engine) as session:
        created = Authors(
            name=data.name
        )
        session.add(created)
        session.commit()
        session.refresh(created)

        return 'Created Successfully'

def create_slot(data : CreateSlot):
    '''This tools is for create slot in Slots Table'''
    with Session(engine) as session:
        created = Slots(
            bookId=data.bookId,
            authorId=data.authorId
        )

        session.add(created)
        session.commit()
        session.refresh(created)

        return 'Created Successfully'

    
def update_user(id : int, data : UpdateUser):
    '''This tool is for update Users table'''
    with Session(engine) as session:
        update = session.get(Users, id)

        if update is None:
            return "UserID Not found in the Database"

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(update, field, value)

        session.add(update)
        session.commit()
        session.refresh(update)

        return 'updated successfully'

def update_book(id : int, data : UpdateBook):
    '''This tool is for update Books table'''
    with Session(engine) as session:
        update = session.get(Books, id)

        if update is None:
            return "BookID Not found in the Database"

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(update, field, value)

        session.add(update)
        session.commit()
        session.refresh(update)

        return 'updated successfully'

def update_author(id : int, data : UpdateAuthor):
    '''This tool is for update Author table'''
    with Session(engine) as session:
        update = session.get(Authors, id)

        if update is None:
            return "AuthorID Not found in the Database"

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(update, field, value)

        session.add(update)
        session.commit()
        session.refresh(update)

        return 'updated successfully'

def update_slot(id : int, data : UpdateSlot):
    '''This tool is for update Slots table'''
    with Session(engine) as session:
        update = session.get(Slots, id)

        if update is None:
            return "SlotID Not found in the Database"

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(update, field, value)

        session.add(update)
        session.commit()
        session.refresh(update)

        return 'updated successfully'

def book_start_from(chr: str):
    """This tool is for getting characters starting with chr."""
    with Session(engine) as session:
        statement = select(Books).where(Books.name.startswith(chr))
        results = session.exec(statement).all()
        return [book.model_dump() for book in results]

def book_end_with(chr: str):
    """This tool helps to get characters ending with chr."""
    with Session(engine) as session:
        statement = select(Books).where(Books.name.endswith(chr))
        results = session.exec(statement).all()
        return [book.model_dump() for book in results]

def total_slots():
    """This tool will help to see how many slots have been booked."""
    with Session(engine) as session:
        statement = select(func.count(Slots.id))
        count = session.exec(statement).one()
        return {"total_slots": int(count)}

def view_genres():
    """This tool will help to see what genres exist."""
    with Session(engine) as session:
        statement = select(Books.genre, func.count(Books.genre).label('Genres')).group_by(Books.genre)
        results = session.exec(statement).all()
        return [{"genre": row[0], "count": row[1]} for row in results]

def search_book(id: int):
    """Tool which will help get a book by using book ID."""
    with Session(engine) as session:
        statement = select(Books).where(Books.id == id)
        results = session.exec(statement).all()
        return [book.model_dump() for book in results]

def search_author(id: int):
    """Tool which will help get an Author by using author ID."""
    with Session(engine) as session:
        statement = select(Authors).where(Authors.id == id)
        results = session.exec(statement).all()
        return [author.model_dump() for author in results]

def search_user(id: int):
    """Tool which will help get a user by using user ID."""
    with Session(engine) as session:
        statement = select(Users).where(Users.id == id)
        results = session.exec(statement).all()
        return [user.model_dump() for user in results]

def search_book_isavail(id: int):
    """This tool will help you find out whether the book slot is available or not."""
    with Session(engine) as session:
        book_slot = session.get(Slots, id)
        if not book_slot:
            return {"error": "Slot not found"}
        return book_slot.model_dump()


def get_all_books():
    """This tool retrieves a list of all books in the database."""
    with Session(engine) as session:
        statement = select(Books)
        results = session.exec(statement).all()
        return [book.model_dump() for book in results]

def get_all_users():
    """This tool retrieves a list of all registered users."""
    with Session(engine) as session:
        statement = select(Users)
        results = session.exec(statement).all()
        return [user.model_dump() for user in results]

def get_all_authors():
    """This tool retrieves a list of all authors."""
    with Session(engine) as session:
        statement = select(Authors)
        results = session.exec(statement).all()
        return [author.model_dump() for author in results]

def get_all_slots():
    """This tool retrieves a list of all booking slots."""
    with Session(engine) as session:
        statement = select(Slots)
        results = session.exec(statement).all()
        return [slot.model_dump() for slot in results]

def delete_user(id: int):
    """This tool is for deleting a user from the Users table."""
    with Session(engine) as session:
        record = session.get(Users, id)
        if record is None:
            return {"error": "UserID not found in the Database"}
        
        session.delete(record)
        session.commit()
        return {"success": f"User with ID {id} has been deleted."}

def delete_book(id: int):
    """This tool is for deleting a book from the Books table."""
    with Session(engine) as session:
        record = session.get(Books, id)
        if record is None:
            return {"error": "BookID not found in the Database"}
        
        session.delete(record)
        session.commit()
        return {"success": f"Book with ID {id} has been deleted."}

def delete_author(id: int):
    """This tool is for deleting an author from the Authors table."""
    with Session(engine) as session:
        record = session.get(Authors, id)
        if record is None:
            return {"error": "AuthorID not found in the Database"}
        
        session.delete(record)
        session.commit()
        return {"success": f"Author with ID {id} has been deleted."}

def delete_slot(id: int):
    """This tool is for deleting a slot from the Slots table."""
    with Session(engine) as session:
        record = session.get(Slots, id)
        if record is None:
            return {"error": "SlotID not found in the Database"}
        
        session.delete(record)
        session.commit()
        return {"success": f"Slot with ID {id} has been deleted."}