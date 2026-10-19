import {useEffect, useState, useRef} from 'react'
import {Link, useSearchParams} from 'react-router-dom'
import {apiFetch, describeError} from './api'
import type {NoteListOut} from './types'

export default function NoteList() {
    const [items, setItems] = useState<NoteListOut['items']>([]);
    const [cursor, setCursor] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loadingMore, setLoadingMore] = useState(false);
    const [loading, setLoading] = useState(true);
    const [searchParams] = useSearchParams();
    const tag = searchParams.get('tag');
    const tagRef = useRef(tag);
    tagRef.current = tag;

    async function load(nextCursor?: string | null) {
        const requestTag = tag;
        setError(null);
        if (nextCursor) setLoadingMore(true); else setLoading(true);
        try {
            const params = new URLSearchParams();
            if (requestTag) params.set('tag', requestTag);
            if (nextCursor) params.set('cursor', nextCursor);
            const qs = params.toString();
            const result = await apiFetch<NoteListOut>(`/notes/${qs ? `?${qs}` : ''}`);
            if (tagRef.current !== requestTag) return;
            setItems(prev => nextCursor ? [...prev, ...result.items] : result.items);
            setCursor(result.next_cursor);
        } catch (err) {
            if (tagRef.current === requestTag) setError(describeError(err));
        } finally {
            if (tagRef.current === requestTag) {
                if (nextCursor) setLoadingMore(false); else setLoading(false);
            }
        }
    }

    useEffect(() => {
        setItems([]);
        setCursor(null);
        setLoadingMore(false);
        load();
    }, [tag]);

    if (loading && items.length === 0) 
        return <p>Loading...</p>;

    if (error && items.length === 0) 
        return <p>{error}</p>;

    if (items.length === 0)
        return tag
            ? <p>No notes tagged <strong>{tag}</strong>. <Link to="/notes">Clear</Link></p>
            : <p>No notes yet.</p>;

    return (
        <div>
            {tag && (
                <p>Filtered by: <strong>{tag}</strong> <Link to="/notes">Clear</Link></p>
            )}
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