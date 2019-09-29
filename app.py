from flask_socketio_lit_html.webcomponent_base import FlaskWelApp, db
from flask import render_template, jsonify, request
from threading import Thread, Event
from requests import get, post
from time import sleep
from random import randint

class Todo(db.Model):
    """Todo webcomponent model"""
    todo = db.Column(db.String(80))
    accountant = db.Column(db.String(80), default="Name")
    progress = db.Column(db.String(4), default="0%")


def data():
    return jsonify([ [str(task.index), task.todo, task.accountant, task.progress] for task in db.session.query(Todo.index, Todo.todo, Todo.accountant, Todo.progress).all() ])

class TodoApp(FlaskWelApp):
    def __init__(self):
        super(TodoApp, self).__init__(__name__)
        # Register <todo-item> webcomponent to use /todo/ endpoint blueprint and custom render from todo.html jinja template
        self.register_blueprint(Todo.configure_blueprint())
        # TodoApp main page
        self.add_url_rule('/', "TodoApp", lambda : render_template('app.html'))
        self.add_url_rule('/data', view_func=data)

if __name__ == "__main__":
    thread_stop_event = Event()
    def mock():
        """Simulate a client generating random data"""
        sleep(2)
        while not thread_stop_event.isSet():
            tasks = get("http://127.0.0.1:5000/Todo/all").json()['items']
            sleep(1)
            for task_number in tasks:
                task = get("http://127.0.0.1:5000/Todo/"+str(task_number)).json()
                # Add some % to the task and POST it
                task['progress'] = str( min(int(task['progress'][0:-1])+randint(0,5), 100) )+'%'
                post("http://127.0.0.1:5000/Todo", json=task)
                sleep(0.2)
    Thread(target = mock).start()
    TodoApp().runApp()
    print("stopping...")
    thread_stop_event.set()
