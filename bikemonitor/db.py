import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # Return a database connection
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    # Close the database connection
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    # Initialize a new database
    db = get_db()

    # Create schema
    with current_app.open_resource('queries/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # Create segments view
    with current_app.open_resource('queries/segments.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)