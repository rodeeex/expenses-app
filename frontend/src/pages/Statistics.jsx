import { useState, useEffect } from "react";
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
} from "@mui/material";
import { expensesAPI } from "../api/expenses";

export const Statistics = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage] = useState(10);
  const [totalStats, setTotalStats] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      const usersData = await expensesAPI.getStatistics();
      setUsers(usersData);

      const totalAmount = usersData.reduce(
        (sum, user) => sum + user.total_amount,
        0,
      );
      const totalCount = usersData.reduce(
        (sum, user) => sum + user.expense_count,
        0,
      );

      setTotalStats({
        total_amount: totalAmount,
        count: totalCount,
      });

      setError("");
    } catch (err) {
      console.error("Error loading statistics:", err);
      setError("Ошибка загрузки статистики");
    } finally {
      setLoading(false);
    }
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const paginatedUsers = users.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage,
  );

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="400px"
      >
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
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

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
                <Typography variant="h4">{users.length}</Typography>
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
                    ? (totalStats.total_amount / users.length).toFixed(2)
                    : "0.00"}{" "}
                  ₽
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>№</TableCell>
                <TableCell>Имя пользователя</TableCell>
                <TableCell align="right">Всего расходов</TableCell>
                <TableCell align="right">Сумма расходов</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedUsers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} align="center">
                    Нет данных
                  </TableCell>
                </TableRow>
              ) : (
                paginatedUsers.map((user, index) => (
                  <TableRow key={user.id} hover>
                    <TableCell>{page * rowsPerPage + index + 1}</TableCell>
                    <TableCell>
                      <Typography fontWeight="medium">
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
