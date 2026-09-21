import {useEffect, useState} from 'react'
import {useParams, useNavigate} from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import {apiFetch, ApiError} from './api'
import type {NoteOut} from './types'

export default function NoteDetail() {
    const {id} = useParams();
    const [note, setNote] = useState<NoteOut | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [deleteError, setDeleteError] = useState("");
    const [deleting, setDeleting] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        setNote(null);
        setError(null);
        apiFetch<NoteOut>(`/notes/${id}`)
            .then(setNote)
            .catch(err => setError(err instanceof ApiError ? err.detail : "Something went wrong"));
    }, [id]);

    async function deleteHandler() {
        if (deleting) return;
        if (!window.confirm("Delete this note?")) return;
        setDeleteError("");
        setDeleting(true);
        try {
            await apiFetch<void>(`/notes/${id}`, {method: 'DELETE'});
            navigate(`/notes`); 
        } catch (err) {
            if (err instanceof ApiError) {
                setDeleteError(err.detail);
            } else if (err instanceof TypeError) {
                setDeleteError("Server unreachable. Try again.");
            } else {
                setDeleteError("Something went wrong");
            }
        } finally {
            setDeleting(false);
        }
    }

    if (error) 
        return <p>{error}</p>;

    if (!note) 
        return <p>Loading...</p>;

    return (
        <div>
            <h2>{note.title}</h2>
            <ReactMarkdown>{note.body}</ReactMarkdown>
            <button disabled={deleting} onClick={deleteHandler}>Delete</button>
            {deleteError && <p>{deleteError}</p>}
        </div>
    );
}