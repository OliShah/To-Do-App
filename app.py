from flask import Flask, jsonify, request, render_template, redirect, url_for
import os
import json

app = Flask(__name__)

DATA = "tasks.json"

def read_tasks():
    if not os.path.exists(DATA):
        return []
    with open(DATA, 'r') as file:
        return json.load(file)

def write_tasks(tasks):
    with open(DATA, 'w') as file:
        json.dump(tasks, file, indent=4)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = read_tasks()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = read_tasks()

    if not request.json:
        return jsonify({"error": "Request body must not be an empty JSON."}), 400
    
    new_task = request.json
    
    new_task['id'] = tasks[-1]['id']+1 if tasks else 1
    new_task['status'] = 'Pending'
    
    tasks.append(new_task)
    write_tasks(tasks)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    tasks = read_tasks()
    task = next((task for task in tasks if task['id']==task_id), None)
    if task:
        return jsonify(task), 200
    return jsonify({'error':'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = read_tasks()
    updated_tasks = [task for task in tasks if task['id']!=task_id]
    if len(tasks)==len(updated_tasks):
        return jsonify({'error':'Task not found'}), 404
    write_tasks(updated_tasks)
    return jsonify({'message':'Task deleted successfully'})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = read_tasks()
    task = next((task for task in tasks if task['id']==task_id), None)
    if not task:
        return jsonify({'error':'Task not found'}), 404
    
    data = request.json
    task.update(data)
    write_tasks(tasks)
    return jsonify(task)

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    tasks = read_tasks()
    task = next((task for task in tasks if task['id']==task_id), None)
    if not task:
        return jsonify({'error':'Task not found'}), 404
    
    task['status'] = 'completed'
    write_tasks(tasks)
    return jsonify(task)

@app.route('/tasks/categories', methods=['GET'])
def get_categories():
    tasks = read_tasks()
    categories = list(set(task['category'] for task in tasks))
    return jsonify(categories)

@app.route('/tasks/categories/<category_name>', methods=['GET'])
def get_tasks_by_category(category_name):
    tasks = read_tasks()
    filtered_tasks = [task for task in tasks if task['category'] == category_name]
    return jsonify(filtered_tasks)

@app.route('/')
def index():
    tasks = read_tasks()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)