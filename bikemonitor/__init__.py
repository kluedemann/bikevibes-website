import os

from flask import Flask


def create_app(test_config=None):
    """
    The Application factory function.
    Sets the configuration and registers blueprints.
    
    Returns: app - a Flask application object
    """

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'bikemonitor.db'),
    )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from bikemonitor import db, upload, map, data, delete
    db.init_app(app)
    app.register_blueprint(upload.bp)
    app.register_blueprint(map.bp)
    app.register_blueprint(data.bp)
    app.register_blueprint(delete.bp)

    return app
