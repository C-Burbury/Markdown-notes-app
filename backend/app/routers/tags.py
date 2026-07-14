from fastapi import APIRouter, Depends, HTTPException
from app.models.tag import Tag,  note_tags
from app.models.note import Note
from app.dependencies import get_current_user
from app.schemas import TagOut, TagCreate
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from app.database import get_db
from app.models.user import User

router = APIRouter(tags=["tags"])

@router.post("/notes/{note_id}/tags", response_model = TagOut, status_code = 201)
def create_tag(data: TagCreate, note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(404)
    
    tag = db.scalar(select(Tag).where(Tag.user_id == current_user.id, Tag.name == data.name))
    if not tag:
        tag = Tag(name=data.name, user_id=current_user.id)
        db.add(tag)
        db.flush()
    
    db.execute(insert(note_tags).values(note_id=note_id, tag_id=tag.id).on_conflict_do_nothing())
    db.commit()

    return tag

@router.get("/notes/{note_id}/tags", response_model = list[TagOut])
def get_tag(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(404)
    
    tags = db.scalars(
        select(Tag)
        .join(note_tags, note_tags.c.tag_id == Tag.id)
        .where(note_tags.c.note_id == note_id, Tag.user_id == current_user.id)
    ).all()
    
    return tags
    
@router.get("/tags", response_model=list[TagOut])
def get_tags(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.scalars(select(Tag).where(Tag.user_id == current_user.id)).all()

@router.delete("/notes/{note_id}/tags/{tag_id}", status_code = 204)
def delete_tag(note_id: int, tag_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(404)
    
    db.execute(delete(note_tags).where(note_tags.c.note_id == note_id, note_tags.c.tag_id == tag_id))
    db.commit()
    return None