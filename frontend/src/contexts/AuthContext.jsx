import { createContext, useState, useEffect } from 'react';
import { authAPI } from '../api/auth';
import { usersAPI } from '../api/users';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const userData = await usersAPI.getCurrentUser();
      setUser(userData);
      setIsAuthenticated(true);
    } catch {
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      await authAPI.login(username, password);
      await checkAuth();
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Ошибка входа',
      };
    }
  };

  const register = async (username, password) => {
    try {
      await authAPI.register(username, password);
      return await login(username, password);
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Ошибка регистрации',
      };
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const updateUser = async (data) => {
    try {
      const updatedUser = await usersAPI.updateCurrentUser(data);
      setUser(updatedUser);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Ошибка обновления профиля',
      };
    }
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
