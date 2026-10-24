from typing import Annotated

from fastapi import Depends

from app.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.user_repository import UserRepository
from app.service.user_auth_service import UserAuthService

DB_Session = Annotated[AsyncSession, Depends(get_db_session)]


def get_user_repository(session: DB_Session) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    session: DB_Session,
    repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserAuthService(session, repository)
