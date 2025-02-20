from flask import Flask, render_template, request, redirect
from models.Todo import db, Todo
import os

app = Flask(__name__)

# Get the database URL from the environment, default to SQLite
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# Ensure no tracking overhead (optional optimization)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def updateTodo(id):
    todo = Todo.query.get_or_404(id)
    print(todo)

    if request.method == 'POST':
        todo.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Error updating todo: {e}'

    return render_template('todo/update.html', todo=todo)

# Zappa Lambda handler
# def handler(event, context):
#     return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)