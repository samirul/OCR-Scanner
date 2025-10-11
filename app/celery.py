import os
from celery import Celery
from celery import shared_task
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
	__name__,
	broker=os.environ.get("CELERY_BROKER_URL"),
	backend=os.environ.get("CELERY_RESULT_BACKEND")
)

celery.autodiscover_tasks(['app.task'])

celery.conf.update(
    task_serializer='json',
	accept_content=['json'],
	result_serializer='json',
	timezone='UTC',
	enable_utc=True,
)

@shared_task(bind=True)
def sum():
    return 5