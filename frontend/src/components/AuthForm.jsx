import { useState } from 'react';

export default function AuthForm({ title, fields, onSubmit, submitLabel, footer }) {
  const [form, setForm] = useState(() => Object.fromEntries(fields.map((field) => [field.name, ''])));
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      await onSubmit(form);
    } catch (err) {
      setError(err?.response?.data?.message || err?.message || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-card">
      <h1>{title}</h1>
      <form onSubmit={handleSubmit} className="auth-form">
        {fields.map((field) => (
          <label key={field.name} className="field">
            <span>{field.label}</span>
            <input
              type={field.type}
              name={field.name}
              value={form[field.name]}
              onChange={handleChange}
              required
            />
          </label>
        ))}
        {error && <p className="error-text">{error}</p>}
        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? 'Please wait...' : submitLabel}
        </button>
      </form>
      {footer}
    </div>
  );
}
