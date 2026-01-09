import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';
import { SignIn } from './pages/SignIn';
import { SignUp } from './pages/SignUp';
import { Profile } from './pages/Profile';
import { MyExpenses } from './pages/MyExpenses';
import { Statistics } from './pages/Statistics';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Публичные маршруты */}
            <Route path="/auth/sign-in" element={<SignIn />} />
            <Route path="/auth/sign-up" element={<SignUp />} />

            {/* Защищенные маршруты */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Statistics />} />
              <Route path="me/profile" element={<Profile />} />
              <Route path="me/expenses" element={<MyExpenses />} />
            </Route>

            {/* Перенаправление на главную для неизвестных маршрутов */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
