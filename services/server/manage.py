from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import Task


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    db.session.add(Task(
        description='Can you please restart our application in dev?',
        team='MMX',
        planned=True
    ))
    db.session.add(Task(
        description='How can I get access to my services in production',
        team='LPM',
        planned=False
    ))
    db.session.add(Task(
        description='Can you please Google this for me',
        team='SPIL',
        planned=True
    ))
    db.session.commit()


if __name__ == '__main__':
    cli()
