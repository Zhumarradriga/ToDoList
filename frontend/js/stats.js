import { apiRequest } from './api.js';

// Функции для работы со статистикой
const stats = {
    async getUserStats() {
        const token = localStorage.getItem('auth_token');
        return apiRequest('stats', '/stats/user/', 'GET', null, token);
    },

    async getTaskStats() {
        const token = localStorage.getItem('auth_token');
        return apiRequest('stats', '/stats/tasks/', 'GET', null, token);
    },

    async getCompletionStats() {
        const token = localStorage.getItem('auth_token');
        return apiRequest('stats', '/stats/completion/', 'GET', null, token);
    }
};

export { stats }; 