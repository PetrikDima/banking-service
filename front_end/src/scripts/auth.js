import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/v1';

export const auth = {

    async register(username, password) {
        try {
            console.info('Credentials', username, password);
            const response = await axios.post(`${API_URL}/users/`, { username, password });
            console.info('Response', response.data);
            return response.data;
        } catch (error) {
            console.error('Error during registration:', error.response ? error.response.data : error);
            throw error;
        }
    },

    async login(username, password) {
        try {
            const response = await axios.post(`${API_URL}/login/`, {
                "username": username,
                "password": password
            });
            console.info(response.data);
            if (response.data.access) {
                localStorage.setItem('user-token', response.data.access);
                return response.data;
            } else {
                throw new Error('No token in response');
            }
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    },

    isAuthenticated() {
        return localStorage.getItem('user-token') !== null;
    },

    logout() {
        localStorage.removeItem('user-token');
    },

    getToken() {
        return localStorage.getItem('user-token');
    }
};
