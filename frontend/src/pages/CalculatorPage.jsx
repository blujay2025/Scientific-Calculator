import { useEffect, useState } from 'react';
import api from '../api';
import Calculator from '../components/Calculator';
import HistoryPanel from '../components/HistoryPanel';
import { useAuth } from '../context/AuthContext';

export default function CalculatorPage() {
  const { user, logout } = useAuth();
  const [history, setHistory] = useState([]);
  const [expression, setExpression] = useState('0');

  const loadHistory = async () => {
    try {
      const response = await api.get('/history');
      setHistory(response.data.history);
    } catch {
      setHistory([]);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleReuse = (item) => {
    setExpression(item.expression || '0');
  };

  const handleDelete = async (id) => {
    await api.delete(`/history/${id}`);
    await loadHistory();
  };

  const handleClear = async () => {
    await api.delete('/history');
    await loadHistory();
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>Scientific Calculator</h1>
          <p>Welcome back, {user?.username}</p>
        </div>
        <button type="button" className="primary-btn" onClick={logout}>Logout</button>
      </header>

      <main className="dashboard-grid">
        <Calculator expression={expression} setExpression={setExpression} onHistoryRefresh={loadHistory} />
        <HistoryPanel items={history} onReuse={handleReuse} onDelete={handleDelete} onClear={handleClear} />
      </main>
    </div>
  );
}
