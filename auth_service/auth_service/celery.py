
import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')

# Создаём экземпляр приложения Celery
app = Celery('auth_service')

# Загружаем настройки Celery из настроек Django (с префиксом CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях (например, в todo_auth/tasks.py)
app.autodiscover_tasks()