from celery import Celery

from api.core import config

broker_url = f'redis://{config.redis_host}:{config.redis_port}'
celery_app = Celery('tasks', broker=broker_url, beat_max_loop_interval=5)
celery_app.autodiscover_tasks(
    [
        'api.monitoring.tasks',
        'api.monitoring.crud'
    ]
)