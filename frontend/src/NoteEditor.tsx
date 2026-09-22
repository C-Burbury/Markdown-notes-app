import {useState, useEffect} from 'react'
import {useNavigate} from 'react-router-dom'
import {apiFetch, describeError} from './api'
import type {NoteOut} from './types'
import {useParams} from 'react-router-dom'

export default function NoteEditor() {
    const [title, setTitle] = useState("");
    const [body, setBody] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [loadError, setLoadError] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [originalTitle, setOriginalTitle] = useState("");
    const [originalBody, setOriginalBody] = useState("");
    const navigate = useNavigate();

    const {id} = useParams();
    const isEdit = Boolean(id);
    const [loading, setLoading] = useState(isEdit);

    useEffect(() => {
        if (!isEdit) return;
        apiFetch<NoteOut>(`/notes/${id}`)
            .then(note => { setTitle(note.title); setBody(note.body); setOriginalTitle(note.title); setOriginalBody(note.body); })
            .catch(err => setLoadError(describeError(err)))
            .finally(() => setLoading(false));
    }, [id, isEdit]);

    async function submitHandler() {
        if (submitting) return;
        if (!title.trim()) {setError("Title required"); return; }
        setError(null);
        setSubmitting(true);
        try {
            if (isEdit) {
                const edits: Record<string, string> = {};
                if (title !== originalTitle) edits.title = title;
                if (body !== originalBody) edits.body = body;
                if (Object.keys(edits).length === 0) {
                    navigate(`/notes/${id}`); 
                    return;
                }
                const note = await apiFetch<NoteOut>(`/notes/${id}`, {
                    method: 'PATCH',
                    body: JSON.stringify({...edits})
                });
                navigate(`/notes/${note.id}`);
            } else {
                const note = await apiFetch<NoteOut>('/notes/', {
                    method: 'POST',
                    body: JSON.stringify({title, body})
                });
                navigate(`/notes/${note.id}`);
            }
            
        } catch (err) {
            setError(describeError(err));
        } finally {
            setSubmitting(false)
        }
    }

    if (loading)
        return (
            <p>Loading...</p>   
        );
    
    if (isEdit && loadError)
        return <p>{loadError}</p>

    return (
        <div>
            <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title"/>
            <textarea value={body} onChange={e => setBody(e.target.value)} placeholder="Body (markdown)"/>
            <button onClick={submitHandler} disabled={submitting}>Save</button>
            {error && <p>{error}</p>}
        </div>
    );
}