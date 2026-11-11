import {useState} from 'react'
import {useNavigate, Link} from 'react-router-dom'
import {useAuth} from './AuthContext'
import {apiFetch, describeError} from './api'
import type {Token, UserOut} from './types'

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    const { login } = useAuth();
    const navigate = useNavigate();

    async function submitHandler() {
        setError(null);
        if (password.length < 8) {
            setError("Password must be at least 8 characters");
            return;
        }

        try {
            await apiFetch<UserOut>('/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) });
            const result = await apiFetch<Token>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
            login(result.access_token); 
            navigate('/notes');
        } catch (err){
            setError(describeError(err));
        }
    }

    return (
        <div className="auth-page">
            <div className="auth">
                <h1>Sign up</h1>
                <div className="field">
                    <label htmlFor="NewEmail">Email</label>
                    <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" autoComplete="email" id="NewEmail"/>
                </div>
                <div className="field">
                    <label htmlFor="NewPassword">Password</label>
                    <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="At least 8 characters" autoComplete="new-password" id="NewPassword"/>
                </div>
                <button onClick={submitHandler}>Sign up</button>
                {error && <p className="error" role="alert">{error}</p>}
                <p>Already have an account? <Link to="/login">Log in</Link></p>
            </div>
        </div>
    );
}