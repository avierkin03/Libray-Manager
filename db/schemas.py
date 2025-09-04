# Тут знаходяться класи, які будуть представляти собою Pydantic моделі

from typing import Union
from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str = Field(min_length = 1, max_length = 100, description = "Назва книги")
    pages: int = Field(default = None, gt = 10, description = "Кількість сторінок (мінімум 10)")


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int
    # конфігурація, яка вказує що ми хочемо зробити Pydantic модель сумісною з ORM
    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str = Field(min_length = 3, max_length = 30, description = "Ім'я автора")


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []
    # конфігурація, яка вказує що ми хочемо зробити Pydantic модель сумісною з ORM
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    login: str


class UserDB(UserBase):
    password: str


class UserCreate(UserBase):
   password: str


class User(UserBase):
   id: int
  
   class Config:
       from_attributed = True