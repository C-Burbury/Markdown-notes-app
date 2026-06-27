from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, DateTime, String, ForeignKey, Text, Computed
from sqlalchemy.dialects.postgresql import TSVECTOR
from datetime import datetime
from typing import Any

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255), server_default=text("'Untitled'"))
    body: Mapped[str] = mapped_column(Text, server_default=text("''"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    tsv: Mapped[Any] = mapped_column(TSVECTOR, Computed("setweight(to_tsvector('english', coalesce(title, '')), 'A') || setweight(to_tsvector('english', coalesce(body, '')), 'B')", persisted=True))