from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vagrant:vagrant@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)

  def __repr__(self):
    return '<Todo %s, %s>' % (self.id, self.description)


@app.route('/')
def index():
  return render_template('index.html', todos=Todo.query.order_by(Todo.id).all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if error:
    abort(400)
  else:
    return jsonify(body)

@app.route('/todos/set-completed/<id>', methods=['POST'])
def set_completed_todo(id):
  error = False
  body = {}
  try:
    newCompleted = request.get_json()['completed']
    todo = Todo.query.get(id)
    todo.completed = newCompleted
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if error:
    abort(400)
  else:
    return jsonify(body)
  



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
