FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Создаем директорию для логов и устанавливаем права
RUN mkdir -p /app/logs && \
    chmod 777 /app/logs

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "auth_service.wsgi:application"]