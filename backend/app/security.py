import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_text: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain_text.encode(), hashed.encode())