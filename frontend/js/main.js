import { apiRequest, getToken } from './api.js';

// Проверка авторизации при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    const token = getToken();
    if (!token) {
        window.location.href = '/Authorization.html';
        return;
    }

    try {
        // Получаем данные пользователя
        const userData = await apiRequest('auth', '/user/', 'GET', null, token);
        
        // Отображаем имя пользователя
        document.querySelector('.user-greeting').textContent = `Привет, ${userData.username}!`;
        
        // Получаем задачи пользователя
        const tasks = await apiRequest('tasks', '/tasks/', 'GET', null, token);
        
        // Обновляем прогресс
        updateProgress(tasks);
        
        // Отображаем задачи
        displayTasks(tasks);
    } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
        alert('Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже.');
    }
});

// Функция обновления прогресса
function updateProgress(tasks) {
    const completedTasks = tasks.filter(task => task.completed).length;
    const totalTasks = tasks.length;
    const progressPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
    
    // Обновляем прогресс-бар
    const progressBar = document.querySelector('.progress-bar');
    progressBar.style.background = `linear-gradient(to right, #562BD7 ${progressPercentage}%, rgba(96, 56, 233, 0.31) ${progressPercentage}%)`;
    
    // Обновляем текст прогресса
    document.querySelector('.progress-text').textContent = `${completedTasks}/${totalTasks}`;
}

// Функция отображения задач
function displayTasks(tasks) {
    const tasksList = document.querySelector('.tasks-list');
    tasksList.innerHTML = ''; // Очищаем список

    tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.className = 'task-item';
        taskElement.innerHTML = `
            <input type="checkbox" ${task.completed ? 'checked' : ''} 
                   onchange="toggleTask('${task.id}', this.checked)">
            <span class="${task.completed ? 'completed' : ''}">${task.title}</span>
            <button onclick="deleteTask('${task.id}')">Удалить</button>
        `;
        tasksList.appendChild(taskElement);
    });
}

// Функция добавления задачи
window.addTask = async () => {
    const taskInput = document.querySelector('#taskInput');
    const title = taskInput.value.trim();
    
    if (!title) {
        alert('Пожалуйста, введите название задачи');
        return;
    }

    try {
        const token = getToken();
        const newTask = await apiRequest('tasks', '/tasks/', 'POST', { title }, token);
        
        // Обновляем список задач
        const tasks = await apiRequest('tasks', '/tasks/', 'GET', null, token);
        displayTasks(tasks);
        updateProgress(tasks);
        
        // Очищаем поле ввода
        taskInput.value = '';
    } catch (error) {
        console.error('Ошибка при добавлении задачи:', error);
        alert('Произошла ошибка при добавлении задачи');
    }
};

// Функция переключения статуса задачи
window.toggleTask = async (taskId, completed) => {
    try {
        const token = getToken();
        await apiRequest('tasks', `/tasks/${taskId}/`, 'PUT', { completed }, token);
        
        // Обновляем список задач
        const tasks = await apiRequest('tasks', '/tasks/', 'GET', null, token);
        updateProgress(tasks);
    } catch (error) {
        console.error('Ошибка при обновлении задачи:', error);
        alert('Произошла ошибка при обновлении задачи');
    }
};

// Функция удаления задачи
window.deleteTask = async (taskId) => {
    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
        return;
    }

    try {
        const token = getToken();
        await apiRequest('tasks', `/tasks/${taskId}/`, 'DELETE', null, token);
        
        // Обновляем список задач
        const tasks = await apiRequest('tasks', '/tasks/', 'GET', null, token);
        displayTasks(tasks);
        updateProgress(tasks);
    } catch (error) {
        console.error('Ошибка при удалении задачи:', error);
        alert('Произошла ошибка при удалении задачи');
    }
}; 