from celery import Celery, Task
from flask import Flask

# runs the task in application context, just running task in application context
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object('config')

    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

