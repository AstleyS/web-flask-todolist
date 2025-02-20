from flask import Flask, render_template, request, redirect
from models.Todo import db, Todo
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

# Initialize the database
db.init_app(app)

# Create tables (for local SQLite use)
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def addTodo():
    if request.method == 'POST':
        content = request.form['content']
        new_todo = Todo(content=content)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Error adding todo: {e}'

    todos = Todo.query.order_by(Todo.date_created).all()
    return render_template('todo/index.html', todos=todos)

@app.route('/delete/<int:id>')
def deleteTodo(id):
    todo = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'Error deleting todo: {e}'

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def updateTodo(id):
    todo = Todo.query.get_or_404(id)
    logging.debug(f'Todo object retrieved: {todo}')

    if request.method == 'POST':
        todo.content = request.form['content']
        logging.debug(f'Updated content: {todo.content}')

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            logging.error(f'Error updating todo: {e}')
            return f'Error updating todo: {e}'

    return render_template('todo/update.html', todo=todo)

# Zappa Lambda handler
# def handler(event, context):
#     return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)