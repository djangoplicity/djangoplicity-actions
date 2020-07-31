from __future__ import absolute_import
from __future__ import print_function
import os
import sys
from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

app = Celery('test_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if 'celery' in sys.argv[0]:
   print('Djangoplicity: Disabling CONN_MAX_AGE')
   settings.DATABASES['default']['CONN_MAX_AGE'] = 0

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))