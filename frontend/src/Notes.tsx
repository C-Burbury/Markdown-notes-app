import {useAuth} from './AuthContext'
import {Outlet} from 'react-router-dom'

export default function Notes() {
    const {logout} = useAuth();
    return (
    <div>Notes page (placeholder)
        <button onClick={logout}>Logout</button>
        <Outlet/>
    </div>);
}