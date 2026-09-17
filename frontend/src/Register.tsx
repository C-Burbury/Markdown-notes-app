import {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import {useAuth} from './AuthContext'
import {apiFetch, ApiError} from './api'
import type {Token, UserOut} from './types'

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    const { login } = useAuth();
    const navigate = useNavigate();

    async function submitHandler() {
        setError(null);

        try {
            await apiFetch<UserOut>('/auth/register', { method: 'POST', body: JSON.stringify({ email, password }) });
             const result = await apiFetch<Token>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
             login(result.access_token); 
             navigate('/notes');
        } catch (err){
            if (err instanceof ApiError) {
                setError(err.detail);
            } else {
                setError("Something went wrong");
            }
        }
    }

    return (
        <div>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email"/>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password"/>
            <button onClick={submitHandler}> Submit</button>
            {error && <p>{error}</p>}
        </div>
    );
}