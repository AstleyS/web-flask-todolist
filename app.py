from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Configurating the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# Model TODO with an id, content and date_created
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # Our toString()
    def __repr__(self):
        return f'<Todo {self.id}>'

# Defining a route in '/' (localhot:<port>/), and especifying the requests methods (from the form or not)
# This function add a todo to the db or just get the todos from the db
@app.route('/', methods = ['POST', 'GET'])
def addTodo():
    # If we request '/' by a POST method it means that are adding a TODO from the form
    if request.method == 'POST':
        content = request.form['content']
        new_todo = Todo(content = content) 
        
        # Trying to connect to the db
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding todo'
    
    # If we request '/' by a GET method
    else:
        # Query all the todos from the database
        todos = Todo.query.order_by(Todo.date_created).all()
        # Render the todos in index.html
        return render_template('todo/index.html', todos = todos)

# Defining a route in '/delete/<id>' (localhot:<port>/delete/<id>)
# This function deletes a todo from the db
@app.route('/delete/<int:id>')
def deleteTodo(id):
    todo = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting the todo'

# Defining a route in '/update/<id>' (localhot:<port>/update/<id>), and especifying the requests methods (from the form or not)
# This function updates a todo from the db
@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def updateTodo(id):
    # Trying to get the todo to be updated. If not in db then sends an 404 error
    todo = Todo.query.get_or_404(id)

    # Submit the update
    if request.method == 'POST':
        todo.content = request.form['content']
         
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error updating todo'
    
    # Getting the todo, and sending/render it in update.html
    else:
        return render_template('todo/update.html', todo = todo)


if __name__ == '__main__':
    app.run(debug=True)