import os
from celery import Celery
from datetime import timedelta


doc_name = os.getenv("DOC_NAME")
sheet_name = os.getenv("sheet_1")
redis_server = os.getenv("REDIS_SERVER")
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_simulation.settings')

# Create Celery application
app = Celery('chatbot_simulation', broker=redis_server)

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Setting up periodic task scheduling
app.conf.beat_schedule = {
    'sync_google_sheet_data_every_2_seconds': {
        'task': 'chatbot.tasks.sync_google_sheet_data',
        'schedule': timedelta(seconds=10),
        'args': (doc_name, sheet_name or ''),
    },
}

# Optional: Task settings for debugging purposes
app.conf.update(
    task_always_eager=False,  # Set to False to use workers for async execution
    task_eager_propagates=True,  # Propagate exceptions when eager mode is True
)

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

# Optional: Set the result backend if you want to store task results
app.conf.result_backend = redis_server
