import apiClient from './client';

export const usersAPI = {
  // Получить текущего пользователя
  getCurrentUser: async () => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  // Обновить текущего пользователя
  updateCurrentUser: async (data) => {
    const response = await apiClient.put('/users/me', data);
    return response.data;
  },

  // Получить пользователя по ID
  getUser: async (userId) => {
    const response = await apiClient.get(`/users/${userId}`);
    return response.data;
  },

  // Удалить пользователя
  deleteUser: async (userId) => {
    const response = await apiClient.delete(`/users/${userId}`);
    return response.data;
  },
};
