import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Создаем директорию для логов
LOGS_DIR = '/app/logs'
os.makedirs(LOGS_DIR, exist_ok=True)

def setup_logging(service_name):
    # Формат логов с дополнительной информацией
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
    # Создаем логгер
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)
    
    try:
        # Обработчик для stdout (для контейнеров)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console_handler)
        
        # Пути к файлам логов
        info_log = os.path.join(LOGS_DIR, f'{service_name}_info.log')
        error_log = os.path.join(LOGS_DIR, f'{service_name}_error.log')
        debug_log = os.path.join(LOGS_DIR, f'{service_name}_debug.log')
        
        # Создаем файлы, если их нет
        for log_file in [info_log, error_log, debug_log]:
            if not os.path.exists(log_file):
                with open(log_file, 'a') as f:
                    pass
                os.chmod(log_file, 0o666)
        
        # Обработчик для INFO и выше
        info_handler = TimedRotatingFileHandler(
            info_log,
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(info_handler)
        
        # Обработчик для ERROR и выше
        error_handler = TimedRotatingFileHandler(
            error_log,
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(error_handler)
        
        # Обработчик для DEBUG
        debug_handler = TimedRotatingFileHandler(
            debug_log,
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(debug_handler)
        
        logger.info(f"Логирование настроено для сервиса {service_name}")
        
    except Exception as e:
        sys.stderr.write(f"Ошибка при настройке логирования: {str(e)}\n")
        raise
    
    return logger 