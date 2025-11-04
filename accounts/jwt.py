from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from django.conf import settings


ALGORITHM = "HS256"
TOKEN_TTL_MINUTES = 60 * 24  # 24 horas
COOKIE_NAME = "jwt"


def _now():
    return datetime.now(timezone.utc)


def generate_token(user) -> str:
    payload = {
        "sub": str(user.id),
        "username": user.get_username(),
        "is_staff": user.is_staff,
        "exp": _now() + timedelta(minutes=TOKEN_TTL_MINUTES),
        "iat": _now(),
        "type": "access",
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    # PyJWT>=2 returns str; ensure str
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def verify_token(token: str) -> Optional[dict]:
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except jwt.PyJWTError:
        return None
