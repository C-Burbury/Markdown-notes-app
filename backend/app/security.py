import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings, ALGORITHM

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_text: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain_text.encode(), hashed.encode())

def create_access_token(subject: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(subject), "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


