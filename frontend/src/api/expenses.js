import apiClient from "./client";

export const expensesAPI = {
  // Получить список расходов с фильтрацией
  getExpenses: async (params = {}) => {
    const response = await apiClient.get("/expenses/", { params });
    return response.data;
  },

  // Получить расход по ID
  getExpense: async (expenseId) => {
    const response = await apiClient.get(`/expenses/${expenseId}`);
    return response.data;
  },

  // Создать расход
  createExpense: async (data) => {
    const response = await apiClient.post("/expenses/", data);
    return response.data;
  },

  // Обновить расход
  updateExpense: async (expenseId, data) => {
    const response = await apiClient.put(`/expenses/${expenseId}`, data);
    return response.data;
  },

  // Удалить расход
  deleteExpense: async (expenseId) => {
    const response = await apiClient.delete(`/expenses/${expenseId}`);
    return response.data;
  },

  // Получить статистику
  getStatistics: async (params = {}) => {
    const response = await apiClient.get("/users/", { params });
    return response.data;
  },
};
