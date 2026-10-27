from typing import Optional

from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import config

passwordhash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return passwordhash.hash(password)


def verify_hashed_password(password: str, hashed_password: str) -> bool:
    return passwordhash.verify(password, hashed_password)


def create_access_token(data: dict, expiration_minutes: Optional[int] = None):
    encode_data = data.copy()

    if expiration_minutes:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=config.jwt_token_expiration_time
        )

    encode_data.update({"exp": expire})

    return jwt.encode(
        payload=encode_data, key=config.secret_key, algorithm=config.jwt_algorithm
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, config.secret_key, algorithms=[config.jwt_algorithm])
