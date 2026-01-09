import apiClient from './client';

export const authAPI = {
  register: async (username, password) => {
    const response = await apiClient.post('/auth/register', {
      username,
      password,
    });
    return response.data;
  },

  login: async (username, password) => {
    const response = await apiClient.post('/auth/login', {
      username,
      password,
    });
    return response.data;
  },

  refresh: async () => {
    const response = await apiClient.post('/auth/refresh');
    return response.data;
  },

  logout: async () => {
    const response = await apiClient.post('/auth/logout');
    return response.data;
  },
};
