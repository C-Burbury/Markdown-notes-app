import {useEffect, useState} from 'react'
import {Link} from 'react-router-dom'
import {apiFetch, ApiError} from './api'
import type {NoteListOut} from './types'

export default function NoteList() {
    const [items, setItems] = useState<NoteListOut['items']>([]);
    const [cursor, setCursor] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loadingMore, setLoadingMore] = useState(false);
    const [loading, setLoading] = useState(true);

    async function load(nextCursor?: string | null) {
        setError(null);
        if (nextCursor) setLoadingMore(true); else setLoading(true);
        try {
            const query = nextCursor ? `?cursor=${encodeURIComponent(nextCursor)}` : '';
            const result = await apiFetch<NoteListOut>(`/notes${query}`);
            setItems(prev => nextCursor ? [...prev, ...result.items] : result.items);
            setCursor(result.next_cursor);
        } catch (err) {
            setError(err instanceof ApiError ? err.detail : "Something went wrong");
        } finally {
            if (nextCursor) setLoadingMore(false); else setLoading(false);
        }
    }

    useEffect(() => { load(); }, [])

    if (loading && items.length === 0) 
        return <p>Loading...</p>;

    if (error && items.length === 0) 
        return <p>{error}</p>;

    if (items.length === 0) 
        return <p>No notes yet.</p>;
    
    return (
        <div>
            <ul>
                {items.map(note => (
                    <li key={note.id}>
                        <Link to={`/notes/${note.id}`}>{note.title}</Link>
                    </li>
                ))}
            </ul>
            {error && <p>{error}</p>}
            {cursor && <button onClick={() => load(cursor)} disabled={loadingMore}>Next Page</button>}
        </div>
    );

}