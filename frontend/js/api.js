// Базовый URL для API (в продакшене все запросы идут через nginx)
const API_BASE_URL = '';  // Пустой URL, так как используем относительные пути

// Функция для выполнения запросов к API
async function apiRequest(service, endpoint, method = 'GET', data = null, token = null) {
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const options = {
        method,
        headers,
        credentials: 'same-origin'  // Используем same-origin для продакшена
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        // Формируем URL с учетом сервиса
        const url = `${API_BASE_URL}/api/${service}${endpoint}`;
        console.log('Отправка запроса:', { url, method, headers, data });
        
        const response = await fetch(url, options);
        console.log('Получен ответ:', response.status);

        // Проверяем тип контента
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Сервер вернул неверный формат данных');
        }
        
        // Пытаемся получить тело ответа как JSON
        const responseData = await response.json();
        console.log('Данные ответа:', responseData);

        if (!response.ok) {
            throw new Error(
                responseData?.detail || 
                responseData?.message || 
                'Произошла ошибка при выполнении запроса'
            );
        }

        return responseData;
    } catch (error) {
        console.error('Ошибка при выполнении запроса:', error);
        if (error.message.includes('JSON')) {
            throw new Error('Ошибка сервера: неверный формат ответа');
        }
        throw error;
    }
}

// Вспомогательные функции для работы с токеном
function saveToken(token) {
    localStorage.setItem('auth_token', token);
}

function getToken() {
    return localStorage.getItem('auth_token');
}

function removeToken() {
    localStorage.removeItem('auth_token');
}

// Экспорт функций
export { 
    apiRequest,
    saveToken,
    getToken,
    removeToken
}; 