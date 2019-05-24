import os

from flask import Blueprint, jsonify, request

from project.api.models import Task
from project import db
from flasgger import swag_from

tasks_blueprint = Blueprint('tasks', __name__)

@tasks_blueprint.route('/tasks', methods=['GET', 'POST'])
@swag_from('tasks.yml')
def all_tasks():
    """ 
    """
    
    response_object = {
        'status': 'success',
        'container_id': os.uname()[1]
    }
    if request.method == 'POST':
        post_data = request.get_json()
        description = post_data.get('description')
        author = post_data.get('author')
        read = post_data.get('read')
        db.session.add(Task(description=description, author=author, read=read))
        db.session.commit()
        response_object['message'] = 'task added!'
    else:
        response_object['tasks'] = [task.to_json() for task in Task.query.all()]
    return jsonify(response_object)


@tasks_blueprint.route('/health', methods=['GET'])
@swag_from('health.yml')
def health():
    """
    """
    return jsonify({
        'status': 'success',
        'message': 'ok!',
        'container_id': os.uname()[1]
    })


@tasks_blueprint.route('/tasks/<task_id>', methods=['PUT', 'DELETE'])
def single_task(task_id):
    """
    """
    response_object = {
      'status': 'success',
      'container_id': os.uname()[1]
    }
    task = task.query.filter_by(id=task_id).first()
    if request.method == 'PUT':
        post_data = request.get_json()
        task.description = post_data.get('description')
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
