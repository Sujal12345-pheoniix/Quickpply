from datetime import datetime, timedelta
from typing import Any

from jose import jwt, JWTError

from app.config import settings


def create_access_token(subject: str, expires_delta: int | None = None) -> str:
    now = datetime.utcnow()
    expire = now + timedelta(minutes=(expires_delta or settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode: dict[str, Any] = {"sub": subject, "exp": int(expire.timestamp()), "iat": int(now.timestamp()), "type": "local"}
    encoded = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
