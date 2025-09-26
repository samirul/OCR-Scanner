import os
from celery import Celery

celery = Celery(
	__name__,
	broker=os.environ.get("CELERY_BROKER_URL"),
	backend=os.environ.get("CELERY_RESULT_BACKEND")
)