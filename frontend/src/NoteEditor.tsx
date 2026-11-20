import {useState, useEffect} from 'react'
import type {SubmitEvent} from 'react'
import {useNavigate, useLocation, useOutletContext} from 'react-router-dom'
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
    const {search} = useLocation();
    const {id} = useParams();
    const {refresh} = useOutletContext<{refresh: () => void}>();
    const isEdit = Boolean(id);
    const [loading, setLoading] = useState(isEdit);

    useEffect(() => {
        if (!isEdit) return;
        apiFetch<NoteOut>(`/notes/${id}`)
            .then(note => { setTitle(note.title); setBody(note.body); setOriginalTitle(note.title); setOriginalBody(note.body); })
            .catch(err => setLoadError(describeError(err)))
            .finally(() => setLoading(false));
    }, [id, isEdit]);

    async function submitHandler(e: SubmitEvent) {
        e.preventDefault();
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
                    navigate({pathname: `/notes/${id}`, search}); 
                    return;
                }
                const note = await apiFetch<NoteOut>(`/notes/${id}`, {
                    method: 'PATCH',
                    body: JSON.stringify({...edits})
                });
                refresh();
                navigate({pathname: `/notes/${note.id}`, search});
            } else {
                const note = await apiFetch<NoteOut>('/notes/', {
                    method: 'POST',
                    body: JSON.stringify({title, body})
                });
                refresh();
                navigate({pathname: `/notes/${note.id}`, search});
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
        <form className="editor" onSubmit={submitHandler}>
            <h2>{isEdit ? "Edit note" : "New note"}</h2>
            <div>
                <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title" aria-label="Title"/>
            </div>
            <div>
                <textarea value={body} onChange={e => setBody(e.target.value)} placeholder="Body (markdown)" aria-label="Body"/>
            </div>
            <div>
            <button className="primary" type="submit" disabled={submitting}>Save</button>
            </div>{error && <p className="error">{error}</p>}
        </form>
    );
}