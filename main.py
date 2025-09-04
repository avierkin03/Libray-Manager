from typing import Annotated
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import crud, models, schemas
from db.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Монтування статичних файлів і шаблонів
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Залежність для бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Константи
SECRET_KEY = "19109197bd5e7c289b92b2b355083ea26c71dee2085ceccc19308a7291b2ea06"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Функція створення JWT
def token_create(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Функція верифікації токена
def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    
    # Отримуємо токен із cookies
    token = request.cookies.get("auth_token")
    if not token:
        raise credentials_exception
    
    # Перевіряємо токен
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Отримуємо користувача з бази даних
    user = crud.get_user(db, login=username)
    if not user:
        raise credentials_exception
    return user


# Маршрут для сторінки входу
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Маршрут для аутентифікації (API)
@app.post("/token")
async def token_get(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): 
    user_data = crud.get_user(db=db, login=form_data.username)
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect login")
    user = crud.authenticate_user(db=db, login=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = token_create(data={"sub": user.login})
    return {"access_token": token, "token_type": "bearer"}


# HTML-обробка входу
@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db=db, login=username, password=password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Невірний логін або пароль"})
    token = token_create(data={"sub": user.login})
    response = templates.TemplateResponse("authors.html", {"request": request, "authors": crud.get_authors(db)})
    # Встановлюємо cookie з токеном
    response.set_cookie(key="auth_token", value=token, httponly=True, samesite="lax")
    return response


# Маршрут для виходу
@app.post("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = templates.TemplateResponse("login.html", {"request": request})
    response.delete_cookie("auth_token")
    return response


# Маршрут для створення користувача
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, login=user.login, password=user.password)


# Сторінка зі списком авторів
@app.get("/authors/", response_class=HTMLResponse)
async def read_authors(request: Request, db: Session = Depends(get_db)):
    authors = crud.get_authors(db)
    return templates.TemplateResponse("authors.html", {"request": request, "authors": authors})


# Сторінка зі списком книг
@app.get("/books/", response_class=HTMLResponse)
async def read_books(request: Request, db: Session = Depends(get_db)):
    books = crud.get_books(db)
    return templates.TemplateResponse("books.html", {"request": request, "books": books})


# Сторінка створення автора
@app.get("/create_author/", response_class=HTMLResponse)
async def create_author_page(request: Request):
    return templates.TemplateResponse("create_author.html", {"request": request})


@app.post("/create_author/", response_class=HTMLResponse)
async def create_author(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    author = schemas.AuthorCreate(name=name)
    crud.create_author(db, author)
    return templates.TemplateResponse("authors.html", {"request": request, "authors": crud.get_authors(db)})


# Сторінка створення книги (вимагає аутентифікацію)
@app.get("/create_book/{author_id}", response_class=HTMLResponse)
async def create_book_page(request: Request, author_id: int, current_user: models.User = Depends(get_current_user)):
    return templates.TemplateResponse("create_book.html", {"request": request, "author_id": author_id})


@app.post("/authors/{author_id}/books/", response_class=HTMLResponse)
async def create_book_for_author(
    request: Request,
    author_id: int,
    title: str = Form(...),
    pages: int = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = schemas.BookCreate(title=title, pages=pages)
    crud.create_author_book(db=db, book=book, author_id=author_id)
    return templates.TemplateResponse("books.html", {"request": request, "books": crud.get_books(db)})


# Видалення книги (вимагає аутентифікацію)
@app.post("/delete_book/{author_id}/{title}", response_class=HTMLResponse)
async def delete_book(
    request: Request,
    author_id: int,
    title: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    crud.delete_author_book(db=db, title=title, author_id=author_id)
    return templates.TemplateResponse("books.html", {"request": request, "books": crud.get_books(db)})


# Видалення автора (вимагає аутентифікацію)
@app.post("/delete_author/{author_id}", response_class=HTMLResponse)
async def delete_author(
    request: Request,
    author_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    crud.delete_author(db=db, author_id=author_id)
    return templates.TemplateResponse("authors.html", {"request": request, "authors": crud.get_authors(db)})