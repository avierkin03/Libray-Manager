# Тут знаходяться класи, які будуть представляти собою моделі SQLAlchemy (Таблиці з БД)

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

# Клас автора
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, unique = True, index = True)

    # забезпечення зв’язку між двома моделями
    books = relationship("Book", back_populates = "parent")


# Клас книги
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, unique = True, index = True)
    pages = Column(Integer, index = True)
    author_id = Column(Integer, ForeignKey("authors.id"))

    # забезпечення зв’язку між двома моделями
    parent = relationship("Author", back_populates="books")


# Клас користувача
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index = True)
    login = Column(String, unique = True, index = True)
    password = Column(String)
    rights = Column(String)