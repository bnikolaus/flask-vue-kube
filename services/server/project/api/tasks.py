import os

from flask import Blueprint, jsonify, request

from project.api.models import Task
from project import db


tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.route('/tasks', methods=['GET', 'POST'])
def all_tasks():
    response_object = {
        'status': 'success',
        'container_id': os.uname()[1]
    }
    if request.method == 'POST':
        post_data = request.get_json()
        title = post_data.get('title')
        author = post_data.get('author')
        read = post_data.get('read')
        db.session.add(task(title=title, author=author, read=read))
        db.session.commit()
        response_object['message'] = 'task added!'
    else:
        response_object['tasks'] = [task.to_json() for task in Task.query.all()]
    return jsonify(response_object)


@tasks_blueprint.route('/tasks/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'container_id': os.uname()[1]
    })


@tasks_blueprint.route('/tasks/<task_id>', methods=['PUT', 'DELETE'])
def single_task(task_id):
    response_object = {
      'status': 'success',
      'container_id': os.uname()[1]
    }
    task = task.query.filter_by(id=task_id).first()
    if request.method == 'PUT':
        post_data = request.get_json()
        task.title = post_data.get('title')
        task.author = post_data.get('author')
        task.read = post_data.get('read')
        db.session.commit()
        response_object['message'] = 'task updated!'
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        response_object['message'] = 'task removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
