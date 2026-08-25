from typing import Optional, List
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column
from pgvector.sqlalchemy import Vector 


class Users(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    mail : str

class Books(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    genre : str
    authorId : Optional[int] = Field(default=None, foreign_key='authors.id')
    desc : str
    desc_vector : List[float] = Field(sa_column=Column(Vector(384))) 

class Authors(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str

class Slots(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    bookId : Optional[int] = Field(default=None, foreign_key='books.id')
    authorId : Optional[int] = Field(default=None, foreign_key='authors.id')


class CreateUser(BaseModel):
    name : str
    mail : str

class UpdateUser(BaseModel):
    name : str
    mail : int

class CreateBook(BaseModel):
    name : str
    authorId : int
    genre : str
    desc : str
    desc_vector : str

class UpdateBook(BaseModel):
    name : str
    authorId : int
    genre : str
    desc : str
    desc_vector : str

class CreateAuthor(BaseModel):
    name : str

class UpdateAuthor(BaseModel):
    name : str

class CreateSlot(BaseModel):
    bookId : int
    authorId : int

class UpdateSlot(BaseModel):
    bookId : int
    authorId : int
