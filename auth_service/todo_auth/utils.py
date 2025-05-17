import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_confirmation_token():
    """Генерирует случайный токен для подтверждения email"""
    return secrets.token_urlsafe(32)

def send_confirmation_email(user):
    """Отправляет email с ссылкой для подтверждения"""
    token = generate_confirmation_token()
    user.email_confirmation_token = token
    user.save()

    confirmation_url = f"http://localhost:8080/confirm-email/{token}"
    
    html_message = f"""
    <h2>Подтверждение email адреса</h2>
    <p>Здравствуйте, {user.username}!</p>
    <p>Для подтверждения вашего email адреса, пожалуйста, перейдите по следующей ссылке:</p>
    <p><a href="{confirmation_url}">Подтвердить email</a></p>
    <p>Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.</p>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        'Подтверждение email адреса',
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    ) 