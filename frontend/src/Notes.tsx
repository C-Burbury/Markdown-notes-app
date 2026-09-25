import {useAuth} from './AuthContext'
import {Outlet, useNavigate, createSearchParams} from 'react-router-dom'
import {useState} from 'react'
import type {SubmitEvent} from 'react'

export default function Notes() {
    const {logout} = useAuth();
    const [text, setText] = useState("");
    const navigate = useNavigate()

    const submit = (e: SubmitEvent) => {
        e.preventDefault();
        const q = text.trim();
        if (!q) return;
        navigate({pathname: '/notes/search', search: createSearchParams({q}).toString()})
    }

    return (
        <div>Notes Page (placeholder)
            <button onClick={logout}>Logout</button>
            <form onSubmit={submit}>
                <input value={text} onChange={e => setText(e.target.value)} />
                <button type="submit">Search</button>
            </form>
            <Outlet/>
        </div>
    );
}