from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import Depends, HTTPException, status
import jwt

from app.core.config import Config
from app.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.token import TokenData
from app.core.security import decode_access_token

from app.repository.user_repository import UserRepository
from app.services.user_auth_service import UserAuthService

DB_Session = Annotated[AsyncSession, Depends(get_db_session)]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={
        "current_user": "Acces current user details",
        "items:read": "Read the items/data",
    },
)


def get_user_repository(session: DB_Session) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    session: DB_Session,
    repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserAuthService(session, repository)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    security_scopes: SecurityScopes,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = decode_access_token(token)

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        scopes = payload.get("scopes", [])

        token_data = TokenData(sub=email, scopes=scopes)

    except (jwt.PyJWTError, Exception):
        raise credentials_exception

    user = await user_repository.get_user_by_email(token_data.sub)

    if user is None:
        raise credentials_exception

    for required_scopes in security_scopes.scopes:
        if required_scopes not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
    return user
