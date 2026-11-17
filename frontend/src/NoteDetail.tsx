import {useEffect, useState, useRef} from 'react'
import {useParams, useNavigate, Link, createSearchParams, useLocation, useOutletContext} from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import {apiFetch, describeError} from './api'
import type {NoteOut, TagOut} from './types'

export default function NoteDetail() {
    const {id} = useParams();
    const [note, setNote] = useState<NoteOut | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [deleteError, setDeleteError] = useState("");
    const [deleting, setDeleting] = useState(false);
    const [tags, setTags] = useState<TagOut[]>([]);
    const [tagsError, setTagsError] = useState("");
    const [newTagName, setNewTagName] = useState("");
    const [addingTag, setAddingTag] =useState(false);
    const headingRef = useRef<HTMLHeadingElement>(null);
    const {refresh} = useOutletContext<{refresh: () => void}>();
    const {search} = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        setNote(null);
        setError(null);
        apiFetch<NoteOut>(`/notes/${id}`)
            .then(setNote)
            .catch(err => setError(describeError(err)));
    }, [id]);

    async function deleteHandler() {
        if (deleting) return;
        if (!window.confirm("Delete this note?")) return;
        setDeleteError("");
        setDeleting(true);
        try {
            await apiFetch<void>(`/notes/${id}`, {method: 'DELETE'});
            refresh();
            navigate({pathname: '/notes', search})
        } catch (err) {
            setDeleteError(describeError(err));
        } finally {
            setDeleting(false);
        }
    }

    function fetchTags() {
        if (!id) return;
        apiFetch<TagOut[]>(`/notes/${id}/tags`)
            .then(setTags)
            .catch(err => setTagsError(describeError(err)));
    }

    useEffect(fetchTags, [id]);

    useEffect(() => {
        headingRef.current?.focus();
    }, [note]);

    async function tagHandler() {
        if (addingTag) return;
        if (!newTagName.trim()) return;
        setTagsError("");
        setAddingTag(true);
        try {
            await apiFetch<TagOut>(`/notes/${id}/tags`, {
                method: 'POST',
                body: JSON.stringify({name: newTagName})
            });
            setNewTagName("");
            fetchTags();
            refresh();
        } catch (err) {
            setTagsError(describeError(err));
        } finally {
            setAddingTag(false);
        }
    }

    async function detachTag(tagId: number) {
        setTagsError("");
        try {
            await apiFetch<void>(`/notes/${id}/tags/${tagId}`, {method: 'DELETE'});
            fetchTags();
            refresh();
        } catch (err) {
            setTagsError(describeError(err));
        }
    }

    if (error) 
        return <p>{error}</p>;

    if (!note) 
        return <p>Loading...</p>;

    return (
        <div>
            <h2 ref={headingRef} tabIndex={-1}>{note.title}</h2>
            <ReactMarkdown>{note.body}</ReactMarkdown>
            <button onClick={() => navigate({pathname: `/notes/${id}/edit`, search})}>Edit</button>
            <button disabled={deleting} onClick={deleteHandler}>Delete</button>
            {deleteError && <p>{deleteError}</p>}
            <ul>
                {tags.map(tag => (
                    <li key={tag.id}>
                        <Link to={{pathname: '/notes', search: createSearchParams({tag: tag.name}).toString()}}>{tag.name}</Link>
                        {' '}<button onClick={() => detachTag(tag.id)}>x</button>
                    </li>
                ))}
            </ul>
            <input value={newTagName} onChange={e => setNewTagName(e.target.value)} placeholder="New tag"/>
            <button onClick={tagHandler} disabled={addingTag}>Add tag</button>
            {tagsError && <p>{tagsError}</p>}

        </div>
    );
}