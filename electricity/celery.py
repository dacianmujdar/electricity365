from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.app.control import Control

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electricity.settings')

from django.conf import settings  # noqa

app = Celery('electricity')

# Used for revoking tasks.
control = Control(app)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
