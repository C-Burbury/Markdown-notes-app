from jwt import InvalidTokenError, decode
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from app.database import get_db
from app.models.user import User
from app.schemas import TokenData
from app.config import settings, ALGORITHM
from sqlalchemy.orm import Session

bearer = HTTPBearer()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"}
)


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
        db: Session = Depends(get_db)
        ) -> User:
    token = credentials.credentials
    try:
        payload = decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception
    
    sub = payload.get("sub")
    try:
        token_data = TokenData(id=sub)
    except ValidationError:
        raise credentials_exception

    user = db.get(User, token_data.id)
    if user is None:
        raise credentials_exception
    
    return user
