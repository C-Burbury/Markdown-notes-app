import {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import {apiFetch, ApiError} from './api'
import type {NoteOut} from './types'

export default function NoteEditor() {
    const [title, setTitle] = useState("");
    const [body, setBody] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    async function submitHandler() {
        if (submitting) return;
        if (!title.trim()) {setError("Title required"); return; }
        setError(null);
        setSubmitting(true);
        try {
            const note = await apiFetch<NoteOut>('/notes/', {
                method: 'POST',
                body: JSON.stringify({title, body})
            });
            navigate(`/notes/${note.id}`);
        } catch (err) {
            if (err instanceof ApiError) {
                setError(err.detail);
            } else if (err instanceof TypeError) {
                setError("Server unreachable. Try again.");
            } else {
                setError("Something went wrong");
            }
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div>
            <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title"/>
            <textarea value={body} onChange={e => setBody(e.target.value)} placeholder="Body (markdown)"/>
            <button onClick={submitHandler} disabled={submitting}>Save</button>
            {error && <p>{error}</p>}
        </div>
    );
}