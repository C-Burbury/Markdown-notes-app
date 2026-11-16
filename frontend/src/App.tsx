import {BrowserRouter, Routes, Route, Navigate, useParams, useLocation} from 'react-router-dom'
import Login from './Login'
import Register from './Register'
import Notes from './Notes'
import ProtectedRoute from './ProtectedRoute'
import NoteEditor from './NoteEditor'
import NoteDetail from './NoteDetail'
import EmptyPane from './EmptyPane'

function EditNoteEditor() {
  const {id} = useParams();
  return <NoteEditor key={id}/>
}

function SearchRedirect() {
  const {search} = useLocation();
  return <Navigate to={{pathname: '/notes', search}} replace />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
        <Route path="/" element={<Navigate to="/notes" replace />} />
        <Route element={<ProtectedRoute/>}>
          
            <Route path="/notes" element={<Notes/>}>
              <Route index element={<EmptyPane/>} />
              <Route path="new" element={<NoteEditor key="new"/>} />
              <Route path="search" element={<SearchRedirect/>} />
              <Route path=":id/edit" element={<EditNoteEditor/>} />
              <Route path=":id" element={<NoteDetail/>} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App