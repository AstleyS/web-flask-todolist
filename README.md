# Flask Todo List Application

This is a simple Todo List application built with Flask, a lightweight web framework for Python. The application allows users to add, update, and delete todo items. The application uses SQLAlchemy for database interactions and is configured to use a database URL from the environment, defaulting to SQLite for local development.

## Features

- Add new todo items
- Update existing todo items
- Delete todo items
- List all todo items

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Flask
- SQLAlchemy
- Gunicorn

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/AstleyS/web-flask-todolist.git
   cd web-flask-todolist
  

2. Create and activate a virtual environment
   ```sh
   python -m venv venv # or python3

3. Install the dependencies
    ```sh
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt # or pip3
   
4. Run the application
    ```sh
    flask run