from celery import shared_task
import requests
from logger import logger

@shared_task
def notify_services_of_new_user(user_id):
    logger.info(f"Начало уведомления сервисов о новом пользователе {user_id}")
    
    try:
        # Уведомляем сервис задач
        logger.debug(f"Отправка запроса в tasks_service для пользователя {user_id}")
        tasks_response = requests.post(
            'http://tasksservice:8001/api/tasks/initialize_user/',
            json={'user_id': user_id}
        )
        if tasks_response.status_code == 200:
            logger.info(f"Успешная инициализация пользователя {user_id} в tasks_service")
        else:
            logger.error(f"Ошибка инициализации пользователя {user_id} в tasks_service. "
                        f"Статус: {tasks_response.status_code}, Ответ: {tasks_response.text}")
        
        # Уведомляем сервис статистики
        logger.debug(f"Отправка запроса в stats_service для пользователя {user_id}")
        stats_response = requests.post(
            'http://statsservice:8002/api/stats/initialize_user/',
            json={'user_id': user_id}
        )
        if stats_response.status_code == 200:
            logger.info(f"Успешная инициализация пользователя {user_id} в stats_service")
        else:
            logger.error(f"Ошибка инициализации пользователя {user_id} в stats_service. "
                        f"Статус: {stats_response.status_code}, Ответ: {stats_response.text}")
            
    except Exception as e:
        logger.exception(f"Критическая ошибка при уведомлении сервисов о новом пользователе {user_id}")
        raise  # Пробрасываем исключение дальше для Celery