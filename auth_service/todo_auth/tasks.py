from celery import shared_task
import requests

@shared_task
def notify_services_of_new_user(user_id):
    requests.post('http://tasks_service:8001/api/initialize_user/', json={'user_id': user_id})
    #requests.post('http://stats_service:8002/api/initialize_user/', json={'user_id': user_id})