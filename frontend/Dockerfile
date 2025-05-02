# Используем nginx в качестве базового образа
FROM nginx:alpine

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем файлы фронтенда в директорию nginx
COPY . /usr/share/nginx/html/

# Открываем порт 80
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"] 