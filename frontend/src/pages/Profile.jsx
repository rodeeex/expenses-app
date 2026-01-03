import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  Grid,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from '@mui/material';
import { Logout as LogoutIcon, Save as SaveIcon } from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';

export const Profile = () => {
  const navigate = useNavigate();
  const { user, updateUser, logout } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
  });
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [logoutDialogOpen, setLogoutDialogOpen] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
    setSuccess('');
  };

  const validateForm = () => {
    if (formData.username && formData.username.length < 3) {
      setError('Имя пользователя должно содержать минимум 3 символа');
      return false;
    }
    if (formData.username && formData.username.includes(' ')) {
      setError('Имя пользователя не должно содержать пробелы');
      return false;
    }
    if (formData.password && formData.password.length < 6) {
      setError('Пароль должен содержать минимум 6 символов');
      return false;
    }
    if (formData.password && formData.password !== formData.confirmPassword) {
      setError('Пароли не совпадают');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Проверяем, что хотя бы одно поле заполнено
    if (!formData.username && !formData.password) {
      setError('Заполните хотя бы одно поле для обновления');
      return;
    }

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const updateData = {};
      if (formData.username) {
        updateData.username = formData.username;
      }
      if (formData.password) {
        updateData.password = formData.password;
      }

      const result = await updateUser(updateData);
      
      if (result.success) {
        setSuccess('Профиль успешно обновлен');
        setFormData({
          username: '',
          password: '',
          confirmPassword: '',
        });
      } else {
        setError(result.error);
      }
    } catch (err) {
      console.error('Profile update error:', err);
      setError('Произошла ошибка при обновлении профиля');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/auth/sign-in');
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Профиль
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Текущая информация
            </Typography>
            <Typography variant="body1" color="text.secondary" gutterBottom>
              <strong>Имя пользователя:</strong> {user?.username}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              <strong>ID:</strong> {user?.id}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Действия
            </Typography>
            <Button
              variant="outlined"
              color="error"
              startIcon={<LogoutIcon />}
              onClick={() => setLogoutDialogOpen(true)}
              fullWidth
            >
              Выйти из аккаунта
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Изменить данные
            </Typography>
            <Divider sx={{ mb: 3 }} />

            {success && (
              <Alert severity="success" sx={{ mb: 2 }}>
                {success}
              </Alert>
            )}

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Новое имя пользователя"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    disabled={loading}
                    helperText="Оставьте пустым, если не хотите менять"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  {/* Пустой блок для выравнивания */}
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    type="password"
                    label="Новый пароль"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    disabled={loading}
                    helperText="Минимум 6 символов"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    type="password"
                    label="Подтвердите новый пароль"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    disabled={loading}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button
                    type="submit"
                    variant="contained"
                    startIcon={<SaveIcon />}
                    disabled={loading}
                  >
                    {loading ? 'Сохранение...' : 'Сохранить изменения'}
                  </Button>
                </Grid>
              </Grid>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Диалог подтверждения выхода */}
      <Dialog
        open={logoutDialogOpen}
        onClose={() => setLogoutDialogOpen(false)}
      >
        <DialogTitle>Выход из аккаунта</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Вы уверены, что хотите выйти из аккаунта?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setLogoutDialogOpen(false)}>
            Отмена
          </Button>
          <Button onClick={handleLogout} color="error" autoFocus>
            Выйти
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
