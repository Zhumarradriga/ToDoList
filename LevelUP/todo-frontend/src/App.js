import React, { useState, useEffect } from 'react';
import './App.css';
import { login, register, logout, getUser } from './api';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));
    const [isLoginForm, setIsLoginForm] = useState(true);
    const [user, setUser] = useState(null);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [rePassword, setRePassword] = useState('');

    useEffect(() => {
        if (isAuthenticated) {
            const fetchUser = async () => {
                setUser(await getUser());
            };
            fetchUser();
        }
    }, [isAuthenticated]);

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            await login(username, password);
            setIsAuthenticated(true);
        } catch (error) {
            alert('Ошибка входа: ' + (error.response?.data?.non_field_errors || 'Неизвестная ошибка'));
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        if (password !== rePassword) {
            alert('Пароли не совпадают');
            return;
        }
        try {
            await register({
                username,
                email,
                first_name: firstName,
                last_name: lastName,
                phone_number: phoneNumber,
                password,
                re_password: rePassword,
            });
            await login(username, password);
            setIsAuthenticated(true);
        } catch (error) {
            alert('Ошибка регистрации: ' + (error.response?.data?.non_field_errors || JSON.stringify(error.response?.data) || 'Неизвестная ошибка'));
        }
    };

    const handleLogout = async () => {
        try {
            await logout();
            setIsAuthenticated(false);
            setUser(null);
        } catch (error) {
            alert('Ошибка выхода');
        }
    };

    const toggleForm = () => {
        setIsLoginForm(!isLoginForm);
        setUsername('');
        setPassword('');
        setEmail('');
        setFirstName('');
        setLastName('');
        setPhoneNumber('');
        setRePassword('');
    };

    return (
        <div className="App">
            {isAuthenticated ? (
                <div>
                    {user && <h1>Привет, {user.first_name}!</h1>}
                    <button onClick={handleLogout} className="logout-button">Выйти</button>
                </div>
            ) : (
                <div className="auth-container">
                    <h2>{isLoginForm ? 'Вход' : 'Регистрация'}</h2>
                    {isLoginForm ? (
                        <form onSubmit={handleLogin}>
                            <input
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Имя пользователя"
                                required
                            />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Пароль"
                                required
                            />
                            <button type="submit">Войти</button>
                            <p>
                                Нет аккаунта? <a href="#" onClick={toggleForm}>Зарегистрироваться</a>
                            </p>
                        </form>
                    ) : (
                        <form onSubmit={handleRegister}>
                            <input
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Имя пользователя"
                                required
                            />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Электронная почта"
                                required
                            />
                            <input
                                value={firstName}
                                onChange={(e) => setFirstName(e.target.value)}
                                placeholder="Имя"
                                required
                            />
                            <input
                                value={lastName}
                                onChange={(e) => setLastName(e.target.value)}
                                placeholder="Фамилия"
                                required
                            />
                            <input
                                value={phoneNumber}
                                onChange={(e) => setPhoneNumber(e.target.value)}
                                placeholder="Номер телефона"
                                required
                            />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Пароль"
                                required
                            />
                            <input
                                type="password"
                                value={rePassword}
                                onChange={(e) => setRePassword(e.target.value)}
                                placeholder="Повторите пароль"
                                required
                            />
                            <button type="submit">Зарегистрироваться</button>
                            <p>
                                Уже есть аккаунт? <a href="#" onClick={toggleForm}>Войти</a>
                            </p>
                        </form>
                    )}
                </div>
            )}
        </div>
    );
}

export default App;