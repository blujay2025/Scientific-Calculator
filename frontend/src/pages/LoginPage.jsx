import { Link, useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async ({ email, password }) => {
    await login(email, password);
    navigate('/');
  };

  return (
    <div className="screen-center">
      <AuthForm
        title="Sign in"
        submitLabel="Login"
        onSubmit={handleSubmit}
        fields={[
          { name: 'email', label: 'Email', type: 'email' },
          { name: 'password', label: 'Password', type: 'password' },
        ]}
        footer={<p className="auth-footer">No account yet? <Link to="/register">Create one</Link></p>}
      />
    </div>
  );
}
