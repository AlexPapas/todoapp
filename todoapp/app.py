from flask import Flask, jsonify, redirect, render_template, request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

# take the name of the file
app = Flask(__name__)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:alex@localhost:5432/todoapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Model {data structure or business logic}
class Todo(db.Model):

    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    # resoves the issue of inheritage for debuging
    def __repr__(self):
        return f"<Todo {self.id} {self.description}>"


# create all tables - if exists - does nothing
db.create_all()


# controller - take input and add it to db
@app.route("/todos/create", methods=["POST"])
def create():
    description = request.get_json()["description"]
    print("description", description)
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return LA({"description": todo.description})


# controller - process the request
@app.route("/")
def index():
    # do a Select * statement
    return render_template("index.html", data=Todo.query.all())


if __name__ == "__main__":
    app.run(debug=True)
