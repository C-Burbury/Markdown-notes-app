import {useState} from 'react'
import type {SubmitEvent} from 'react'
import {useNavigate, Link} from 'react-router-dom'
import {useAuth} from './AuthContext'
import {apiFetch, describeError} from './api'
import type {Token} from './types'

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    const { login } = useAuth();
    const navigate = useNavigate();

    async function submitHandler(e: SubmitEvent) {
        e.preventDefault();
        setError(null);

        try {
             const result = await apiFetch<Token>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) });
             login(result.access_token);
             navigate('/notes');
        } catch (err) {
            setError(describeError(err));
        }
    }
    
    return (
        <form className="auth-page" onSubmit={submitHandler}>
            <div className="auth">
                <h1>Log in</h1>
                <div className="field">
                    <label htmlFor="LoginEmail">Email</label>
                    <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" autoComplete="email" id="LoginEmail"/>
                </div>
                <div className="field">
                    <label htmlFor="LoginPassword">Password</label>
                    <input type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" id="LoginPassword"/>
                </div>
                <button type="submit">Log in</button>
                {error && <p className="error" role="alert">{error}</p>}
                <p>Don't have an account? <Link to="/register">Sign up</Link></p>
            </div>
        </form>
    );
}
