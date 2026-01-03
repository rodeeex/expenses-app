import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
} from '@mui/material';
import { expensesAPI } from '../api/expenses';

// Моковые данные для демонстрации, пока нет эндпоинта для получения списка пользователей
const generateMockUsers = () => {
  const names = [
    'Богдан Некрасов', 'Даниил Желанов', 'Антон Пушкарев', 'Анна Смирнова',
    'Алексей Козлов', 'Елена Новикова', 'Дмитрий Морозов', 'Ольга Волкова',
    'Сергей Соколов', 'Наталья Лебедева', 'Андрей Егоров', 'Татьяна Павлова',
    'Михаил Семенов', 'Екатерина Федорова', 'Владимир Васильев', 'Юлия Михайлова',
    'Николай Попов', 'Светлана Новикова', 'Игорь Захаров', 'Виктория Романова',
    'Артем Кузнецов', 'Дарья Соловьева', 'Максим Борисов', 'Ксения Григорьева',
    'Денис Степанов', 'Александра Николаева', 'Роман Орлов', 'Марина Белова',
  ];

  return names.map((name, index) => ({
    id: `user-${index + 1}`,
    username: name.toLowerCase().replace(' ', '_'),
    displayName: name,
    total_amount: Math.random() * 100000 + 10000,
    expense_count: Math.floor(Math.random() * 200) + 10,
  }));
};

export const Statistics = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage] = useState(10);
  const [totalStats, setTotalStats] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Загружаем общую статистику
      const stats = await expensesAPI.getStatistics();
      setTotalStats(stats);

      // TODO: Когда будет готов эндпоинт для получения списка пользователей,
      // заменить моковые данные на реальные
      // const usersData = await usersAPI.getAllUsers();
      
      // Пока используем моковые данные
      const mockUsers = generateMockUsers();
      setUsers(mockUsers);
      
    } catch (err) {
      console.error('Error loading statistics:', err);
      setError('Ошибка загрузки статистики');
      
      // Даже при ошибке показываем моковые данные для демонстрации
      const mockUsers = generateMockUsers();
      setUsers(mockUsers);
    } finally {
      setLoading(false);
    }
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  // Пагинация
  const paginatedUsers = users.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Статистика по всем пользователям
      </Typography>

      {error && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          {error} (показаны демонстрационные данные)
        </Alert>
      )}

      {/* Общая статистика */}
      {totalStats && (
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Общая сумма расходов
                </Typography>
                <Typography variant="h4">
                  {totalStats.total_amount.toFixed(2)} ₽
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {totalStats.count} записей
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Пользователей в системе
                </Typography>
                <Typography variant="h4">
                  {users.length}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Средний расход на пользователя
                </Typography>
                <Typography variant="h4">
                  {users.length > 0
                    ? (users.reduce((sum, u) => sum + u.total_amount, 0) / users.length).toFixed(2)
                    : '0.00'} ₽
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Таблица пользователей */}
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>№</TableCell>
                <TableCell>Пользователь</TableCell>
                <TableCell>Имя пользователя</TableCell>
                <TableCell align="right">Всего расходов</TableCell>
                <TableCell align="right">Сумма расходов</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedUsers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} align="center">
                    Нет данных
                  </TableCell>
                </TableRow>
              ) : (
                paginatedUsers.map((user, index) => (
                  <TableRow key={user.id} hover>
                    <TableCell>{page * rowsPerPage + index + 1}</TableCell>
                    <TableCell>
                      <Typography fontWeight="medium">
                        {user.displayName}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" color="text.secondary">
                        {user.username}
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="body2">
                        {user.expense_count} записей
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography fontWeight="bold">
                        {user.total_amount.toFixed(2)} ₽
                      </Typography>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          component="div"
          count={users.length}
          page={page}
          onPageChange={handleChangePage}
          rowsPerPage={rowsPerPage}
          rowsPerPageOptions={[10]}
          labelDisplayedRows={({ from, to, count }) =>
            `${from}-${to} из ${count}`
          }
          labelRowsPerPage="Записей на странице:"
        />
      </Paper>
    </Box>
  );
};

