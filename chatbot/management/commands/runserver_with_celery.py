import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Starts the Django development server, Celery worker, and Celery Beat scheduler'

    def handle(self, *args, **kwargs):
        try:
            # Start the Celery worker in a separate process
            celery_worker = subprocess.Popen(['celery', '-A', 'chatbot_simulation', 'worker', '--loglevel=info', '-P', 'solo'])
            self.stdout.write(self.style.SUCCESS('Celery worker started successfully.'))

            # Start the Celery Beat scheduler in a separate process
            celery_beat = subprocess.Popen(['celery', '-A', 'chatbot_simulation', 'beat', '--loglevel=info'])
            self.stdout.write(self.style.SUCCESS('Celery Beat scheduler started successfully.'))

            # Start the Django development server
            os.system('python manage.py runserver')

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
