import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async register(credentials) {
      try {
        await apiClient.post('/auth/register', credentials);
        await this.login({
          username: credentials.email,
          password: credentials.password,
        });
      } catch (error) {
        console.error('Registration failed:', error.response.data);
        throw error.response.data;
      }
    },
    async login(credentials) {
      try {
        const formData = new URLSearchParams();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);

        const { data } = await apiClient.post('/auth/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        this.token = data.access_token;
        localStorage.setItem('token', data.access_token);

        const userResponse = await apiClient.get('/users/me');
        this.user = userResponse.data;
        localStorage.setItem('user', JSON.stringify(userResponse.data));

        router.push('/dashboard');
      } catch (error) {
        console.error('Login failed:', error.response.data);
        throw error.response.data;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    },
  },
});
