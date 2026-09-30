import {BrowserRouter, Routes, Route, Navigate, useParams} from 'react-router-dom'
import Login from './Login'
import Register from './Register'
import Notes from './Notes'
import ProtectedRoute from './ProtectedRoute'
import NoteList from './NoteList'
import NoteEditor from './NoteEditor'
import NoteDetail from './NoteDetail'
import SearchScreen from './SearchScreen'

function EditNoteEditor() {
  const {id} = useParams();
  return <NoteEditor key={id}/>
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
              <Route index element={<NoteList/>} />
              <Route path="new" element={<NoteEditor key="new"/>} />
              <Route path="search" element={<SearchScreen/>} />
              <Route path=":id/edit" element={<EditNoteEditor/>} />
              <Route path=":id" element={<NoteDetail/>} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App