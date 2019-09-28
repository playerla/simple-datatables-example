from flask_socketio_lit_html.webcomponent_base import FlaskWelApp, db
from flask import render_template, jsonify, request

class Todo(db.Model):
    """Todo webcomponent model"""
    todo = db.Column(db.String(80))
    accountant = db.Column(db.String(80), default="Bastien")


def data():
    return jsonify([ [task.todo,task.accountant] for task in db.session.query(Todo.todo, Todo.accountant).all() ])

class TodoApp(FlaskWelApp):
    def __init__(self):
        super(TodoApp, self).__init__(__name__)
        # Register <todo-item> webcomponent to use /todo/ endpoint blueprint and custom render from todo.html jinja template
        self.register_blueprint(Todo.configure_blueprint())
        # TodoApp main page
        self.add_url_rule('/', "TodoApp", lambda : render_template('app.html'))
        self.add_url_rule('/data', view_func=data)

if __name__ == "__main__":
    TodoApp().runApp()