# Library Manager

Library Manager is a web application built with FastAPI, SQLAlchemy, and Jinja2 templates for managing a library's authors and books. It includes user authentication using JWT tokens, allowing secure access to create, view, and delete authors and books.

## Features
- User authentication with JWT tokens stored in cookies.
- Create, view, and delete authors and books.
- Secure routes for creating and deleting resources, accessible only to authenticated users.
- SQLite database for storing users, authors, and books.
- Responsive HTML templates with Jinja2 for rendering the UI.
- Password hashing using `passlib` with bcrypt for secure user authentication.

## Project Structure
```
Library Manager/
├── db/
│   ├── __init__.py
│   ├── crud.py         # Database operations (CRUD)
│   ├── database.py     # Database setup and configuration
│   ├── models.py       # SQLAlchemy models
│   ├── schemas.py      # Pydantic schemas for validation
├── static/             # Static files (CSS, JS, etc.)
├── templates/          # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── authors.html
│   ├── books.html
│   ├── create_author.html
│   ├── create_book.html
├── main.py             # FastAPI application
├── README.md           # Project documentation
```

## Requirements
- Python 3.8+
- Dependencies (listed in `requirements.txt`):
  - `fastapi`
  - `sqlalchemy`
  - `jose[python-jwt]`
  - `passlib[bcrypt]`
  - `jinja2`
  - `python-multipart`

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_username/library-manager.git
   cd library-manager
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```
   The application will be available at `http://localhost:8000`.

## Usage
1. **Access the application**:
   - Open `http://localhost:8000` in your browser to view the login page.
   - Log in with a valid username and password (create a user via the `/users/` endpoint if needed).

2. **Features**:
   - **Login**: Authenticate using the login form (`/login`).
   - **Authors**: View the list of authors (`/authors`), add new authors (`/create_author`), or delete existing ones.
   - **Books**: View the list of books (`/books`), add new books for a specific author (`/create_book/{author_id}`), or delete books.
   - **Logout**: Log out to clear the authentication cookie (`/logout`).

3. **API Endpoints**:
   - `POST /token`: Authenticate and receive a JWT token.
   - `POST /users/`: Create a new user.
   - `POST /create_author/`: Create a new author.
   - `POST /authors/{author_id}/books/`: Create a book for a specific author.
   - `POST /delete_book/{author_id}/{title}`: Delete a book.
   - `POST /delete_author/{author_id}`: Delete an author.

## Database
- The application uses SQLite (`library.db`) for data storage.
- Tables are automatically created on startup (`models.Base.metadata.create_all`).
- Models include `User`, `Author`, and `Book` with relationships defined in `models.py`.

## Security
- Passwords are hashed using bcrypt (`passlib`).
- Authentication is handled via JWT tokens stored in HTTP-only cookies.
- Protected routes (`/create_book`, `/delete_book`, `/delete_author`) require a valid JWT token.

## Templates
- The application uses Jinja2 templates for rendering HTML pages.
- `base.html`: Base template with navigation.
- `login.html`: Login page.
- `authors.html`: Displays the list of authors.
- `books.html`: Displays the list of books.
- `create_author.html`: Form to create a new author.
- `create_book.html`: Form to create a new book.

## Running Tests
- Ensure all dependencies are installed.
- Use a testing framework like `pytest` to write and run tests (not included in this project).


## Screenshots

### Authors List Page
![Authors_Page Screenshot](screenshots/authors_page.png)

### Page for adding a new author
![add_author_page Screenshot](screenshots/add_author_page.png)

### Books List Page
![Books_Page Screenshot](screenshots/books_page.png)

### Login Page
![Login_Page Screenshot](screenshots/login_page.png)