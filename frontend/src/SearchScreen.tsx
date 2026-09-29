import {useEffect, useState, useRef} from 'react'
import {Link, useSearchParams} from 'react-router-dom'
import {apiFetch, describeError} from './api'
import type {SearchListOut} from './types'

function Headline({text}: {text: string}) {
    const parts = text.split(/<mark>|<\/mark>/)
    return (
        <>
            {parts.map((part, i) =>
                i % 2 === 1 ? <mark key={i}>{part}</mark> : <span key={i}>{part}</span>
            )}
        </>
    )
}

export default function SearchScreen() {
    const [params] = useSearchParams();
    const q = params.get('q')

    const [items, setItems] = useState<SearchListOut['items']>([]);
    const [cursor, setCursor] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [loadingMore, setLoadingMore] = useState(false);
    const [loadMoreError, setLoadMoreError] = useState<string | null>(null);
    const qRef = useRef(q);
    qRef.current = q;

    useEffect(() => {
        setItems([]);
        setCursor(null);
        setError(null);
        setLoading(false);
        setLoadingMore(false);
        setLoadMoreError(null);
        if (!q) return;

        let ignore = false;
        setLoading(true);

        const load = async () => {
            try {
                const query = new URLSearchParams({q}).toString();
                const result = await apiFetch<SearchListOut>(`/search/?${query}`);
                if (ignore) return;
                setItems(result.items);
                setCursor(result.next_cursor);
            } catch (err) {
                if (!ignore) setError(describeError(err));
            } finally {
                if (!ignore) setLoading(false);
            }
        };

        load();
        return () => {ignore = true};
    }, [q]);

    async function loadMore() {
        if (!cursor || loadingMore) return;
        const requestQ = q;
        setLoadMoreError(null);
        setLoadingMore(true);
        try {
            const query = new URLSearchParams({q: requestQ!, cursor}).toString();
            const result = await apiFetch<SearchListOut>(`/search/?${query}`);
            if (qRef.current !== requestQ) return;
            setItems(prev => [...prev, ...result.items]);
            setCursor(result.next_cursor);
        } catch (err) {
            if (qRef.current === requestQ) setLoadMoreError(describeError(err));
        } finally {
            if (qRef.current === requestQ) setLoadingMore(false);
        }
    }

    if (!q) return <p>Enter a search.</p>;
    if (loading) return <p>Loading...</p>;
    if (error) return <p>{error}</p>;
    if (items.length === 0) return <p>No results.</p>;

    return (
        <>
            <ul>
                {items.map(r => (
                    <li key={r.id}>
                        <Link to={`/notes/${r.id}`}>{r.title}</Link>
                        <p><Headline text={r.headline}/></p>
                    </li>
                ))}
            </ul>
            {loadMoreError && <p>{loadMoreError}</p>}
            {cursor && <button onClick={loadMore} disabled={loadingMore}>Load more</button>}
        </>
    )
}