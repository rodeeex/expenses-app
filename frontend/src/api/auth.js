import apiClient from './client';

export const authAPI = {
  // Регистрация
  register: async (username, password) => {
    const response = await apiClient.post('/auth/register', {
      username,
      password,
    });
    return response.data;
  },

  // Вход
  login: async (username, password) => {
    const response = await apiClient.post('/auth/login', {
      username,
      password,
    });
    return response.data;
  },

  // Обновление токена
  refresh: async () => {
    const response = await apiClient.post('/auth/refresh');
    return response.data;
  },

  // Выход
  logout: async () => {
    const response = await apiClient.post('/auth/logout');
    return response.data;
  },
};
