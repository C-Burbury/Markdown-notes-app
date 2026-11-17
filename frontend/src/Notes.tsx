import {useAuth} from './AuthContext'
import {Outlet, useNavigate, createSearchParams, useSearchParams, useLocation, Link} from 'react-router-dom'
import {useState, useCallback} from 'react'
import type {SubmitEvent} from 'react'
import NoteList from "./NoteList"
import SearchScreen from "./SearchScreen"

export default function Notes() {
    const {logout} = useAuth();
    const [text, setText] = useState("");
    const navigate = useNavigate()
    const [searchParams] = useSearchParams();
    const query = searchParams.get('q')
    const [version, setVersion] = useState(0);
    const {search, pathname} = useLocation();
    const detailOpen = pathname !== '/notes';

    const refresh = useCallback(() => {
        setVersion(v => v + 1);
    }, []);


    const submit = (e: SubmitEvent) => {
        e.preventDefault();
        const q = text.trim();
        if (!q) return;
        navigate({pathname: '/notes', search: createSearchParams({q}).toString()})
    }
        

    return (
        <div>
            <header>
                <h1>Markdown Notes</h1>
                <button onClick={logout}>Logout</button>
                <button onClick={() => navigate('/notes')}>All notes</button>
                <button onClick={() => navigate({pathname: '/notes/new', search})}>New note</button>
                <form onSubmit={submit}>
                    <input value={text} onChange={e => setText(e.target.value)} placeholder ="Search notes..." aria-label="Search notes..."/>
                    <button type="submit">Search</button>
                </form>
            </header>
            <div className={detailOpen ? 'workspace detail-open' : 'workspace'}>
                <nav aria-label="Notes">
                    {query ? <SearchScreen version={version}/> : <NoteList version={version}/>}
                </nav>
                <main>{detailOpen && 
                    <Link className="back-link" to={{pathname: '/notes', search}}>Back to notes</Link>}
                    <Outlet context={{refresh}}/>
                </main>   
            </div>
        </div>
    );
}