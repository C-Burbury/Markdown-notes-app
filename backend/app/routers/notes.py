from fastapi import APIRouter, Depends, HTTPException
from app.models.note import Note
from app.dependencies import get_current_user
from app.schemas import NoteCreate, NoteOut, NoteUpdate
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model = NoteOut, status_code = 201)
def create(data: NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = Note(**data.model_dump(), user_id=current_user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.get("/{note_id}", response_model = NoteOut)
def get_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if note is None or note.user_id != current_user.id:
        raise HTTPException(status_code=404)
    return note

@router.patch("/{note_id}", response_model = NoteOut)
def update_note(payload: NoteUpdate, note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if note is None or note.user_id != current_user.id:
        raise HTTPException(status_code=404)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}", status_code = 204)
def delete_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if note is None or note.user_id != current_user.id:
        raise HTTPException(status_code=404)
    db.delete(note)
    db.commit()
    return None