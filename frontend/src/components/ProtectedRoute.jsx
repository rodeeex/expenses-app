import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Box, CircularProgress } from '@mui/material';

export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  // ВРЕМЕННО: Отключаем проверку авторизации для просмотра UI
  // TODO: Включить обратно когда backend будет готов
  return children;

  /* Раскомментировать когда backend заработает:
  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth/sign-in" replace />;
  }

  return children;
  */
};
