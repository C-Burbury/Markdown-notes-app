from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id: int

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    body: str = ""

class NoteUpdate(BaseModel):
    title: str  | None = Field(default=None, min_length=1, max_length=255)
    body: str | None = None

class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    body: str
    created_at: datetime
    updated_at: datetime

class NoteListOut(BaseModel):
    items: list[NoteOut]
    next_cursor: str | None = None