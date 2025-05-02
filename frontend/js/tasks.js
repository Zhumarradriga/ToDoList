import { apiRequest } from './api.js';

// Функции для работы с задачами
const tasks = {
    async getAllTasks() {
        const token = localStorage.getItem('auth_token');
        return apiRequest('tasks', '/tasks/', 'GET', null, token);
    },

    async createTask(title, description, dueDate) {
        const token = localStorage.getItem('auth_token');
        return apiRequest('tasks', '/tasks/', 'POST', { title, description, due_date: dueDate }, token);
    },

    async updateTask(taskId, data) {
        const token = localStorage.getItem('auth_token');
        return apiRequest('tasks', `/tasks/${taskId}/`, 'PUT', data, token);
    },

    async deleteTask(taskId) {
        const token = localStorage.getItem('auth_token');
        return apiRequest('tasks', `/tasks/${taskId}/`, 'DELETE', null, token);
    },

    async getTaskById(taskId) {
        const token = localStorage.getItem('auth_token');
        return apiRequest('tasks', `/tasks/${taskId}/`, 'GET', null, token);
    }
};

export { tasks }; 