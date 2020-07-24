from __future__ import print_function
from celery import shared_task


@shared_task
def hello():
    print('Hello there!')