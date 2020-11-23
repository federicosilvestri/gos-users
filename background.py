from gooutsafe import create_app, create_celery

flask_app = create_app()
app = create_celery(flask_app)

try:
    import gooutsafe.tasks
except ImportError:
    raise RuntimeError('Cannot import celery tasks')
