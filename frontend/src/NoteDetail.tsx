import {useEffect, useState} from 'react'
import {useParams} from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import {apiFetch, ApiError} from './api'
import type {NoteOut} from './types'

export default function NoteDetail() {
    const {id} = useParams();
    const [note, setNote] = useState<NoteOut | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setNote(null);
        setError(null);
        apiFetch<NoteOut>(`/notes/${id}`)
            .then(setNote)
            .catch(err => setError(err instanceof ApiError ? err.detail : "Something went wrong"));
    }, [id]);

    if (error) 
        return <p>{error}</p>;

    if (!note) 
        return <p>Loading...</p>;

    return (
        <div>
            <h2>{note.title}</h2>
            <ReactMarkdown>{note.body}</ReactMarkdown>
        </div>
    );
}