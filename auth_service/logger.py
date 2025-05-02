from logging_config import setup_logging

# Создаем логгер для сервиса аутентификации
logger = setup_logging('auth_service')

# Примеры использования логгера в коде:
# logger.debug("Отладочное сообщение")
# logger.info("Информационное сообщение")
# logger.warning("Предупреждение")
# logger.error("Ошибка")
# logger.critical("Критическая ошибка")

# Для логирования исключений:
# try:
#     # код
# except Exception as e:
#     logger.exception("Произошла ошибка при аутентификации") 