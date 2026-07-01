from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.note import Note
from app.dependencies import get_current_user
from app.schemas import SearchListOut
from sqlalchemy import select, tuple_, func
from app.database import get_db
import json, base64

router = APIRouter(prefix="/search")

@router.get("/", response_model=SearchListOut)
def get_search_list(
    q: str = Query(..., min_length=1), 
    page_limit: int = Query(default=20, ge=1, le=100), 
    cursor: str | None = None, 
    current_user = Depends(get_current_user), 
    db = Depends(get_db)):
        
        tsq = func.websearch_to_tsquery('english', q)
        rank_expr = func.ts_rank_cd(Note.tsv, tsq, 1) 
        stmt = select(
            Note.id,
            Note.title, 
            rank_expr.label('rank'),
            func.ts_headline('english', Note.body, tsq).label('headline')
        )

        stmt = stmt.where(Note.user_id == current_user.id).where(Note.tsv.op('@@')(tsq))
        stmt = stmt.order_by(rank_expr.desc(), Note.id.desc())

        cursor_rk = cursor_id = None
        if cursor is not None:
            try:
                data = json.loads(base64.urlsafe_b64decode(cursor).decode())
                cursor_rk = data["rank"]
                cursor_id = data["id"]
            except (ValueError, KeyError):
                raise HTTPException(status_code=400, detail="Invalid cursor")
        
        if cursor_rk is not None and cursor_id is not None:
            stmt = stmt.where(
                tuple_(rank_expr, Note.id) < (cursor_rk, cursor_id)
            )

        stmt = stmt.limit(page_limit + 1)
        notes = db.execute(stmt).all()
        has_next = len(notes) > page_limit
        notes = notes[:page_limit]

        if has_next:
            last = notes[-1]
            payload = {"rank": last.rank, "id": last.id}
            next_cursor = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
        else:
            next_cursor = None
        
        return SearchListOut(items=notes, next_cursor=next_cursor)