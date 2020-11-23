"""
Flask initialization
"""
import os

__version__ = '0.1'

import connexion
from flask_environments import Environments
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging

db = None
migrate = None
debug_toolbar = None
redis_client = None
app = None
api_app = None
logger = None
celery = None


def create_app():
    """
    This method create the Flask application.
    :return: Flask App Object
    """
    global db
    global app
    global migrate
    global api_app

    # first initialize the logger
    init_logger()

    api_app = connexion.FlaskApp(
        __name__,
        server='flask',
        specification_dir='openapi/',
    )

    # getting the flask app
    app = api_app.app

    flask_env = os.getenv('FLASK_ENV', 'None')
    if flask_env == 'development':
        config_object = 'config.DevConfig'
    elif flask_env == 'testing':
        config_object = 'config.TestConfig'
    elif flask_env == 'production':
        config_object = 'config.ProdConfig'
    else:
        raise RuntimeError(
            "%s is not recognized as valid app environment. You have to setup the environment!" % flask_env)

    # Load config
    env = Environments(app)
    env.from_object(config_object)

    # creating redis instance
    create_redis(app)

    # loading communications
    import gooutsafe.comm as comm

    if flask_env != 'production':
        # disable communication for testing purposes
        comm.disabled = True
    else:
        comm.init_rabbit_mq(app)

    # registering db
    db = SQLAlchemy(
        app=app
    )

    # requiring the list of models
    import gooutsafe.models

    # creating migrate
    migrate = Migrate(
        app=app,
        db=db
    )

    # checking the environment
    if flask_env == 'testing':
        # we need to populate the db
        db.create_all()

    # registering to api app all specifications
    register_specifications(api_app)

    return app


def create_redis(_app):
    global redis_client

    # loading redis
    from flask_redis import FlaskRedis

    if app.config['TESTING']:
        # loading mockredis
        from mockredis import MockRedis
        redis_client = MockRedis(FlaskRedis.from_custom_provider(MockRedis))
    else:
        # loading the real redis instance
        redis_client = FlaskRedis(app)


def create_celery(_app):
    # As celery message broker
    # we use redis instead of
    # RabbitMQ
    global celery

    from celery import Celery
    celery = Celery(
        _app.name,
        broker=_app.config['REDIS_URL'],
        backend=_app.config['REDIS_URL']
    )

    celery.conf.timezone = 'Europe/Rome'
    celery.conf.update(_app.config)

    """
       Importing the tasks with celery
       """
    import gooutsafe.tasks

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with _app.app_context():
                return self.run(*args, **kwargs)

    return celery


def init_logger():
    global logger
    """
    Initialize the internal application logger.
    :return: None
    """
    logger = logging.getLogger(__name__)
    from flask.logging import default_handler
    logger.addHandler(default_handler)


def register_specifications(_api_app):
    """
    This function registers all resources in the flask application
    :param _api_app: Flask Application Object
    :return: None
    """

    # we need to scan the specifications package and add all yaml files.
    from importlib_resources import files
    folder = files('gooutsafe.specifications')
    for _, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = folder.joinpath(file)
                _api_app.add_api(file_path)
