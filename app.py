# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import Schema
from service import ToDoService
import json

app = Flask(__name__)  # create an app instance


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/", methods=["GET"])
def list_todo():
    return render_template('todo_list.html', todos=ToDoService().list())


@app.route("/todo/<item_id>", methods=["GET"])
def list_todo_item(item_id):
    todo_item = ToDoService().get_by_id(item_id)
    if len(todo_item) > 0:
        return render_template('todo_item.html', todo_item=ToDoService().get_by_id(item_id)[0])
    else:
        return redirect(url_for('list_todo'))


@app.route("/todo", methods=["POST"])
def create_todo():
    new_todo = {}
    if request.get_json() is None:
        new_todo['Title'] = request.form['Title']
        new_todo['Description'] = request.form['Description']
        new_todo['DueDate'] = request.form['DueDate']
    else:
        new_todo = request.get_json()

    new_id = ToDoService().create(new_todo)

    return redirect(url_for('list_todo_item', item_id=new_id))


@app.route("/add", methods=["GET"])
def add_todo():
    return render_template('addtodo.html')


@app.route("/update/<item_id>", methods=["POST"])
def update_item(item_id):
    update_todo = {}
    if request.get_json() is None:
        update_todo['Title'] = request.form['Title']
        update_todo['Description'] = request.form['Description']
        update_todo['DueDate'] = request.form['DueDate']
        ToDoService().update(item_id, update_todo)
        return redirect(url_for('list_todo_item', item_id=item_id))
    else:
        update_todo = request.get_json()
        return jsonify(ToDoService().update(item_id, update_todo))


@app.route("/edit/<item_id>")
def edit_item(item_id):
    todo_item = ToDoService().get_by_id(item_id)
    if len(todo_item) > 0:
        return render_template('edit.html', todo_item=ToDoService().get_by_id(item_id)[0])
    else:
        return redirect(url_for('list_todo'))


@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    ToDoService().delete(item_id)
    return redirect(url_for('list_todo'))


@app.route("/delete/<int:item_id>")
def process_delete_item(item_id):
    ToDoService().delete(item_id)
    return redirect(url_for('list_todo'))


@app.route("/done/<int:item_id>")
def process_done_item(item_id):
    ToDoService().done(item_id)
    return redirect(url_for('list_todo'))


if __name__ == "__main__":  # on running python app.py
    Schema()
    app.run(debug=True)  # run the flask app
