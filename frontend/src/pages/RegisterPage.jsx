import { Link, useNavigate } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import { useAuth } from '../context/AuthContext';

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async ({ username, email, password }) => {
    await register({ username, email, password });
    navigate('/');
  };

  return (
    <div className="screen-center">
      <AuthForm
        title="Create account"
        submitLabel="Register"
        onSubmit={handleSubmit}
        fields={[
          { name: 'username', label: 'Username', type: 'text' },
          { name: 'email', label: 'Email', type: 'email' },
          { name: 'password', label: 'Password', type: 'password' },
        ]}
        footer={<p className="auth-footer">Already registered? <Link to="/login">Sign in</Link></p>}
      />
    </div>
  );
}
