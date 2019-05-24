import datetime

from flask import current_app
from sqlalchemy.sql import func

from project import db


class Task(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    read = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, description, author, read):
        self.description = description
        self.author = author
        self.read = read

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'author': self.author,
            'read': self.read
        }
