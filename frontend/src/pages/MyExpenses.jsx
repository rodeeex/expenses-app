import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Grid,
  Alert,
  Chip,
  Card,
  CardContent,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale/ru';
import { expensesAPI } from '../api/expenses';
import { useAuth } from '../hooks/useAuth';

const CATEGORIES = [
  { value: 'food', label: 'Еда' },
  { value: 'transport', label: 'Транспорт' },
  { value: 'subscriptions', label: 'Подписки' },
  { value: 'health', label: 'Здоровье' },
  { value: 'entertainment', label: 'Развлечения' },
  { value: 'utilities', label: 'Коммунальные услуги' },
  { value: 'other', label: 'Другое' },
];

const PAYMENT_METHODS = [
  { value: 'cash', label: 'Наличные' },
  { value: 'card', label: 'Карта' },
  { value: 'other', label: 'Другое' },
];

const getCategoryLabel = (value) => {
  return CATEGORIES.find(c => c.value === value)?.label || value;
};

const getPaymentMethodLabel = (value) => {
  return PAYMENT_METHODS.find(p => p.value === value)?.label || value;
};

export const MyExpenses = () => {
  const { user } = useAuth();
  const [expenses, setExpenses] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [editingExpense, setEditingExpense] = useState(null);
  const [expenseToDelete, setExpenseToDelete] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [formData, setFormData] = useState({
    category: 'food',
    payment_method: 'card',
    amount: '',
    date: new Date().toISOString().split('T')[0],
    comment: '',
  });

  useEffect(() => {
    loadExpenses();
    loadStatistics();
  }, [user]);

  const loadExpenses = async () => {
    if (!user) return;
    
    try {
      setLoading(true);
      const data = await expensesAPI.getExpenses({ user_id: user.id });
      setExpenses(data);
    } catch (err) {
      console.error('Error loading expenses:', err);
      setError('Ошибка загрузки расходов');
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    if (!user) return;
    
    try {
      const data = await expensesAPI.getStatistics({ user_id: user.id });
      setStatistics(data);
    } catch (err) {
      console.error('Error loading statistics:', err);
    }
  };

  const handleOpenDialog = (expense = null) => {
    if (expense) {
      setEditingExpense(expense);
      setFormData({
        category: expense.category,
        payment_method: expense.payment_method,
        amount: expense.amount.toString(),
        date: expense.date,
        comment: expense.comment || '',
      });
    } else {
      setEditingExpense(null);
      setFormData({
        category: 'food',
        payment_method: 'card',
        amount: '',
        date: new Date().toISOString().split('T')[0],
        comment: '',
      });
    }
    setDialogOpen(true);
    setError('');
    setSuccess('');
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingExpense(null);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async () => {
    setError('');
    setSuccess('');

    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      setError('Введите корректную сумму');
      return;
    }

    try {
      const expenseData = {
        ...formData,
        amount: parseFloat(formData.amount),
        user_id: user.id,
      };

      if (!expenseData.comment) {
        delete expenseData.comment;
      }

      if (editingExpense) {
        await expensesAPI.updateExpense(editingExpense.id, expenseData);
        setSuccess('Расход обновлен');
      } else {
        await expensesAPI.createExpense(expenseData);
        setSuccess('Расход добавлен');
      }

      handleCloseDialog();
      await loadExpenses();
      await loadStatistics();
    } catch (err) {
      console.error('Error saving expense:', err);
      setError(err.response?.data?.detail || 'Ошибка сохранения расхода');
    }
  };

  const handleDeleteClick = (expense) => {
    setExpenseToDelete(expense);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!expenseToDelete) return;

    try {
      await expensesAPI.deleteExpense(expenseToDelete.id);
      setSuccess('Расход удален');
      setDeleteDialogOpen(false);
      setExpenseToDelete(null);
      await loadExpenses();
      await loadStatistics();
    } catch (err) {
      console.error('Error deleting expense:', err);
      setError('Ошибка удаления расхода');
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Мои расходы
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Добавить расход
        </Button>
      </Box>

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>
          {success}
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}

      {/* Статистика */}
      {statistics && (
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Всего расходов
                </Typography>
                <Typography variant="h4">
                  {statistics.total_amount.toFixed(2)} ₽
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {statistics.count} записей
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  По категориям
                </Typography>
                {Object.entries(statistics.by_category).map(([cat, amount]) => (
                  <Box key={cat} display="flex" justifyContent="space-between" mt={1}>
                    <Typography variant="body2">{getCategoryLabel(cat)}:</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {amount.toFixed(2)} ₽
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  По способам оплаты
                </Typography>
                {Object.entries(statistics.by_payment_method).map(([method, amount]) => (
                  <Box key={method} display="flex" justifyContent="space-between" mt={1}>
                    <Typography variant="body2">{getPaymentMethodLabel(method)}:</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {amount.toFixed(2)} ₽
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Таблица расходов */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Дата</TableCell>
              <TableCell>Категория</TableCell>
              <TableCell>Сумма</TableCell>
              <TableCell>Способ оплаты</TableCell>
              <TableCell>Комментарий</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  Загрузка...
                </TableCell>
              </TableRow>
            ) : expenses.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  Нет расходов
                </TableCell>
              </TableRow>
            ) : (
              expenses.map((expense) => (
                <TableRow key={expense.id}>
                  <TableCell>
                    {format(new Date(expense.date), 'dd MMMM yyyy', { locale: ru })}
                  </TableCell>
                  <TableCell>
                    <Chip label={getCategoryLabel(expense.category)} size="small" />
                  </TableCell>
                  <TableCell>
                    <Typography fontWeight="bold">
                      {expense.amount.toFixed(2)} ₽
                    </Typography>
                  </TableCell>
                  <TableCell>{getPaymentMethodLabel(expense.payment_method)}</TableCell>
                  <TableCell>{expense.comment || '—'}</TableCell>
                  <TableCell align="right">
                    <IconButton
                      size="small"
                      onClick={() => handleOpenDialog(expense)}
                      color="primary"
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDeleteClick(expense)}
                      color="error"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Диалог создания/редактирования */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingExpense ? 'Редактировать расход' : 'Добавить расход'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  select
                  fullWidth
                  label="Категория"
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                >
                  {CATEGORIES.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  select
                  fullWidth
                  label="Способ оплаты"
                  name="payment_method"
                  value={formData.payment_method}
                  onChange={handleChange}
                >
                  {PAYMENT_METHODS.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Сумма"
                  name="amount"
                  value={formData.amount}
                  onChange={handleChange}
                  inputProps={{ min: 0, step: 0.01 }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="date"
                  label="Дата"
                  name="date"
                  value={formData.date}
                  onChange={handleChange}
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Комментарий"
                  name="comment"
                  value={formData.comment}
                  onChange={handleChange}
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Отмена</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingExpense ? 'Сохранить' : 'Добавить'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Диалог подтверждения удаления */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Удалить расход?</DialogTitle>
        <DialogContent>
          <Typography>
            Вы уверены, что хотите удалить этот расход?
          </Typography>
          {expenseToDelete && (
            <Box mt={2}>
              <Typography variant="body2" color="text.secondary">
                {getCategoryLabel(expenseToDelete.category)} — {expenseToDelete.amount} ₽
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Отмена</Button>
          <Button onClick={handleDeleteConfirm} color="error">
            Удалить
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

