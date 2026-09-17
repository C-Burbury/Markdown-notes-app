import {useAuth} from './AuthContext'

export default function Notes() {
    const {logout} = useAuth();
    return (
    <div>Notes page (placeholder)
        <button onClick={logout}>Logout</button>
    </div>);
}