# скрипт crud.py для взаємодії з даними в базі

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext


# створюємо контекст PassLib для хешування та перевірки паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функція, яка повертає конкретного юзера (по його логіну)
def get_user(db: Session, login: str):
   return db.query(models.User).filter(models.User.login == login).first()


# Функція, яка повертає конкретного юзера після аутентифікації по логіну а пародю
def authenticate_user(db: Session, login: str, password: str):
    user = get_user(db, login)

    # якщо  користувача з таким лгіном не існує
    if not user:
       return False
    # якщо наданий пароль не співпав з реальним паролем користувача (перевірка хешів паролів)
    if not pwd_context.verify(password, user.password):
       return False
    
    return user


# Функція, яка створює нового юзера і додає його в базу даних
def create_user(db: Session, login: str, password: str, rights: str = "user"):
    # хешуємо пароль перед додаванням в базу даних
    hashed_password = pwd_context.hash(password)
    db_user = models.User(login=login, password=hashed_password, rights=rights)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Функція, яка повертає конкретного автора (по його id)
def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


# Функція, яка повертає всіх авторів
def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


# Функція, яка створює нового автора і додає його в базу даних
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name = author.name)
    # додавання екземпляра db_department до сеансу бази даних
    db.add(db_author)
    # фіксація змін в базі даних (щоб вони були збережені)
    db.commit()
    # оновлення екземпляру db_department (щоб він містив будь-які нові дані з бази даних, наприклад згенерований ідентифікатор)
    db.refresh(db_author)
    return db_author


# Функція, яка повертає всі книги
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


# Функція, яка створює нову книгу у конкретного автора
def create_author_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.dict(), author_id = author_id)
    # додавання екземпляра db_product до сеансу бази даних
    db.add(db_book)
    # фіксація змін в базі даних (щоб вони були збережені)
    db.commit()
    # оновлення екземпляру db_product (щоб він містив будь-які нові дані з бази даних, наприклад згенерований ідентифікатор)
    db.refresh(db_book)
    return db_book


# Функція, яка видаляє книгу у конкретного автора
def delete_author_book(db: Session, title: str, author_id: int):
    db_book = db.query(models.Book).filter(models.Book.title == title, models.Book.author_id == author_id).first()

    if db_book is None:
        return {"message": "Book or author was not found"}
    
    db.delete(db_book)
    # фіксація змін в базі даних (щоб вони були збережені)
    db.commit()
    return {"message": "Book was deleted successfully"}


# Функція, яка видаляє конкретного автора
def delete_author(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(models.Author.id == author_id,).first()
    if db_author is None:
        return {"message": "Author was not found"}
    
    db.delete(db_author)
    # фіксація змін в базі даних (щоб вони були збережені)
    db.commit()
    return {"message": "Author was deleted successfully"}