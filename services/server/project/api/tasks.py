import os

from flask import Blueprint, jsonify, request

from project.api.models import Task
from project import db


Tasks_blueprint = Blueprint('Tasks', __name__)


@Tasks_blueprint.route('/Tasks', methods=['GET', 'POST'])
def all_Tasks():
    response_object = {
        'status': 'success',
        'container_id': os.uname()[1]
    }
    if request.method == 'POST':
        post_data = request.get_json()
        title = post_data.get('title')
        author = post_data.get('author')
        read = post_data.get('read')
        db.session.add(Task(title=title, author=author, read=read))
        db.session.commit()
        response_object['message'] = 'Task added!'
    else:
        response_object['Tasks'] = [Task.to_json() for Task in Task.query.all()]
    return jsonify(response_object)


@Tasks_blueprint.route('/Tasks/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'container_id': os.uname()[1]
    })


@Tasks_blueprint.route('/Tasks/<Task_id>', methods=['PUT', 'DELETE'])
def single_Task(Task_id):
    response_object = {
      'status': 'success',
      'container_id': os.uname()[1]
    }
    Task = Task.query.filter_by(id=Task_id).first()
    if request.method == 'PUT':
        post_data = request.get_json()
        Task.title = post_data.get('title')
        Task.author = post_data.get('author')
        Task.read = post_data.get('read')
        db.session.commit()
        response_object['message'] = 'Task updated!'
    if request.method == 'DELETE':
        db.session.delete(Task)
        db.session.commit()
        response_object['message'] = 'Task removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
