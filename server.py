import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

# Initialize Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Define a model for the 'todo' table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Define a route for the root page
@app.route('/', methods=['GET'])
def index():
    # Retrieve all 'todo' items from the database and render the HTML template with the items
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

# Define a route to add a new 'todo' item
@app.route("/add", methods=["POST"])
def add():
    try:
        # Retrieve the title from the form data and create a new 'todo' object with the title and 'complete' set to False
        title = request.form.get("title")
        new_todo = Todo(title=title, complete = False)
        # Add the new 'todo' object to the session and commit the transaction
        db.session.add(new_todo)
        db.session.commit()
        # Redirect to the root page
        return redirect(url_for("index"))
    except:
        # Roll back the transaction if an error occurred
        db.session.rollback()

# Define a route to update the 'complete' status of a 'todo' item
@app.route("/update/<int:todo_id>", methods=["POST"])
def update(todo_id):
    try:
        # Retrieve the 'todo' item with the given ID and update its 'complete' status
        todo = Todo.query.filter_by(id=todo_id).first()
        todo.complete = request.form.get("complete") == "true"
        # Commit the transaction and redirect to the root page
        db.session.commit()
        return redirect(url_for("index"))
    except:
        # Roll back the transaction if an error occurred
        db.session.rollback()


# Define a route to delete a 'todo' item
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    try:
        # Retrieve the 'todo' item with the given ID and delete it from the database
        todo = Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        # Commit the transaction and redirect to the root page
        db.session.commit()
        return redirect(url_for("index"))
    except:
        # Roll back the transaction if an error occurred
        db.session.rollback()

# Define a route to delete all 'todo' items from the database
@app.route("/deletealltodos")
def deleteall():
    try:
        # Delete all 'todo' items from the database
        db.session.query(Todo).delete()
        # Commit the transaction and redirect to the root page
        db.session.commit()
        return redirect(url_for("index"))
    except:
        # Roll back the transaction if an error occurred
        db.session.rollback()

# Start the Flask application
if (__name__ == '__main__'):
    app.run(host="0.0.0.0", port=5000, debug=True)
