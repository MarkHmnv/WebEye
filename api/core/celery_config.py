from celery import Celery

from api.core import config
import api.monitoring.tasks

broker_url = f'redis://{config.redis_host}:{config.redis_port}'
celery_app = Celery('tasks', broker=broker_url, beat_max_loop_interval=5)
