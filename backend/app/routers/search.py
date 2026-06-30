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

router = APIRouter(prefix="/search")


@router.get("")
def get_search_list():
    return {}
    