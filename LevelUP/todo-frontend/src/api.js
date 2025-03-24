import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';
const AUTH_URL = 'http://127.0.0.1:8000/auth/';
let token = localStorage.getItem('token') || null;

const api = axios.create({
    baseURL: API_URL,
    headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use(config => {
    if (token) config.headers.Authorization = `Token ${token}`;
    return config;
});

export const register = async (userData) => {
    const response = await axios.post(`${AUTH_URL}users/`, userData);
    return response.data;
};

export const login = async (username, password) => {
    const response = await axios.post(`${AUTH_URL}token/login/`, { username, password });
    token = response.data.auth_token;
    localStorage.setItem('token', token);
    return response.data;
};

export const logout = async () => {
    await axios.post(`${AUTH_URL}token/logout/`, {}, {
        headers: { Authorization: `Token ${token}` }
    });
    token = null;
    localStorage.removeItem('token');
};

export const getUser = () => api.get('users/').then(res => res.data[0]);
export const getTodoLists = () => api.get('todo-lists/').then(res => res.data);
export const createTodoList = (listData) => api.post('todo-lists/', listData).then(res => res.data);