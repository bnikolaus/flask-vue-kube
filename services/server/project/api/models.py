import datetime

from flask import current_app
from sqlalchemy.sql import func

from project import db


class Task(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    team = db.Column(db.String(255), nullable=False)
    planned = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, description, team, planned, type):
        self.description = description
        self.team = team
        self.planned = planned
        self.type = type

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'team': self.team,
            'planned': self.planned,
            'type': self.type
        }
