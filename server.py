from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

#Setup Flask
app = Flask(__name__)

#DB conf
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()



@app.before_first_request
def create_tables():
    db.create_all()


#DB class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


#Root page
@app.route('/', methods=['GET'])
def index():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    try:
        title = request.form.get("title")
        new_todo = Todo(title=title, complete = False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        db.session.rollback()


@app.route("/update/<int:todo_id>")
def update(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        todo.complete = not todo.complete
        db.session.commit()
        return redirect(url_for("index"))
    except:
        db.session.rollback()


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        db.session.rollback()

@app.route("/deletealltodos")
def deleteall():
    try:
        db.session.query(Todo).delete()
        db.session.commit()
        return redirect(url_for("index"))
    except:
        db.session.rollback()


if (__name__ == '__main__'):
    app.run(debug=True)

