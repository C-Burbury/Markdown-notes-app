import {useSearchParams} from 'react-router-dom'

export default function SearchScreen() {
    const [params] = useSearchParams();
    return (
        <div>q: {params.get('q')}</div>
    );
}