"""
WSGI config for tasks_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from logging_config import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasks_service.settings')

# Инициализация логирования
logger = setup_logging('tasks_service')
logger.info('Tasks service started')

application = get_wsgi_application()
