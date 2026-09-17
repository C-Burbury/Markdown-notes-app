import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom'
import Login from './Login'
import Register from './Register'
import Notes from './Notes'
import ProtectedRoute from './ProtectedRoute'


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
        <Route path="/" element={<Navigate to="/notes" replace />} />
        <Route element={<ProtectedRoute/>}>
          <Route path="/notes" element={<Notes/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App