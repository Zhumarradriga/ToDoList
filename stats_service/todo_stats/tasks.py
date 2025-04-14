from celery import shared_task
from django.conf import settings
from .models import Stat, UserStat


@shared_task
def notify_services_of_new_user(user_id):
    """
    Отправляет сообщение о новом пользователе через Celery
    """
    from celery import current_app
    current_app.send_task('tasks_service.tasks.initialize_user', args=[user_id])


@shared_task
def create_default_stats_for_user(user_id):
    """
    Создает стандартную статистику для нового пользователя
    """
    default_stats = [
        {
            'name': 'Completed Tasks',
            'color': '#4CAF50',
            'icon_id': 1
        },
        {
            'name': 'Experience Gained',
            'color': '#2196F3',
            'icon_id': 2
        },
        {
            'name': 'Tasks Streak',
            'color': '#FFC107',
            'icon_id': 3
        }
    ]
    
    for stat_data in default_stats:
        stat = Stat.objects.create(
            user_id=user_id,
            name=stat_data['name'],
            description=stat_data['name'],
            is_default=True,
            value=0
        )
        UserStat.objects.create(user_id=user_id, stat=stat, value=0)


@shared_task
def update_user_level(user_id, exp_points, current_level):
    """
    Обновляет уровень пользователя на основе накопленного опыта
    """
    # Формула расчета уровня: уровень = корень(опыт / 100)
    import math
    new_level = math.floor(math.sqrt(exp_points / 100))
    
    # Если уровень изменился, обновляем статистику
    if new_level > current_level:
        # Создаем или обновляем статистику уровня
        level_stat = Stat.objects.get_or_create(
            user_id=user_id,
            name='Current Level',
            defaults={
                'description': 'Current user level',
                'is_default': True,
                'value': new_level
            }
        )[0]
        
        user_stat, _ = UserStat.objects.get_or_create(
            user_id=user_id,
            stat=level_stat,
            defaults={'value': new_level}
        )
        user_stat.value = new_level
        user_stat.save() 