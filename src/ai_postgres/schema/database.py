from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Users(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    mail : str

class Books(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    genre : str
    authorId : int

class Authors(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str

class Slots(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    bookId : int
    authorId : int


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

class UpdateBook(BaseModel):
    name : str
    authorId : int
    genre : str

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

