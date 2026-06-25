from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.note import Note
from app.models.tag import Tag, note_tags
from app.dependencies import get_current_user
from app.schemas import NoteCreate, NoteOut, NoteUpdate, NoteListOut
from sqlalchemy.orm import Session
from sqlalchemy import select, tuple_
from app.database import get_db
from app.models.user import User
from datetime import datetime
import json, base64


router = APIRouter(prefix="/notes", tags=["notes"])
PAGE_SIZE = 20

@router.post("/", response_model = NoteOut, status_code = 201)
def create(data: NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = Note(**data.model_dump(), user_id=current_user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.get("/", response_model = NoteListOut)
def get_note_list(cursor: str | None = None, page_limit: int = Query(default=PAGE_SIZE, ge=1, le=100,), 
    created_after: datetime | None = None, created_before: datetime | None = None,
    sort: str = Query(default="desc", pattern="^(asc|desc)$",), tag: str | None = None,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cursor_ts = cursor_id = None
    if cursor is not None:
        try:
            data = json.loads(base64.urlsafe_b64decode(cursor).decode())
            cursor_ts = datetime.fromisoformat(data["ts"])
            cursor_id = data["id"]
        except (ValueError, KeyError):
            raise HTTPException(status_code=400, detail="Invalid cursor")
    asc = sort == "asc"
    stmt = select(Note).where(Note.user_id == current_user.id)
    if cursor_ts is not None and cursor_id is not None:
        if asc:
            stmt = stmt.where(tuple_(Note.created_at, Note.id) > (cursor_ts, cursor_id))
        else:
            stmt = stmt.where(tuple_(Note.created_at, Note.id) < (cursor_ts, cursor_id))
    if created_after is not None:
        stmt = stmt.where(Note.created_at >= created_after)
    if created_before is not None:
        stmt = stmt.where(Note.created_at <= created_before)
    if tag is not None:
        stmt = stmt.where(
            Note.id.in_(
                select(note_tags.c.note_id)
                .join(Tag, Tag.id == note_tags.c.tag_id)
                .where(Tag.name == tag, Tag.user_id == current_user.id)
            )
        )
    if asc:
        stmt = stmt.order_by(Note.created_at.asc(), Note.id.asc())
    else:
        stmt = stmt.order_by(Note.created_at.desc(), Note.id.desc())
    stmt = stmt.limit(page_limit + 1)
    notes = db.execute(stmt).scalars().all()
    has_next = len(notes) > page_limit
    notes = notes[:page_limit]
    if has_next:
        last = notes[-1]
        payload = {"ts": last.created_at.isoformat(), "id": last.id}
        next_cursor = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    else:
        next_cursor = None
    return NoteListOut(items=notes, next_cursor=next_cursor)

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