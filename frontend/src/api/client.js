import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Создаем экземпляр axios
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Важно для отправки HTTP-Only cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// Флаг для предотвращения множественных запросов на обновление токена
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

// Interceptor для обработки ответов
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Если получили 401 и это не запрос на refresh и не повторный запрос
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (originalRequest.url?.includes('/auth/refresh')) {
        // Если refresh токен невалиден, перенаправляем на логин
        isRefreshing = false;
        processQueue(error, null);
        window.location.href = '/auth/sign-in';
        return Promise.reject(error);
      }

      if (isRefreshing) {
        // Если уже идет процесс обновления токена, добавляем запрос в очередь
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(() => {
            return apiClient(originalRequest);
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Пытаемся обновить токен
        await apiClient.post('/auth/refresh');
        isRefreshing = false;
        processQueue(null, null);
        
        // Повторяем оригинальный запрос
        return apiClient(originalRequest);
      } catch (refreshError) {
        isRefreshing = false;
        processQueue(refreshError, null);
        
        // Если не удалось обновить токен, перенаправляем на логин
        window.location.href = '/auth/sign-in';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
