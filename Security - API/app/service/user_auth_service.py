from fastapi import HTTPException, status

from app.core.security import hash_password, verify_hashed_password
from app.repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserLogin


class UserAuthService:
    def __init__(self, session: AsyncSession, repository: UserRepository):
        self.session = session
        self.repository = repository

    async def auth_signup(self, user):
        async with self.session.begin():
            hashed_password = hash_password(user.password)
            user.password = hashed_password
            return await self.repository.create_user(user)

    async def auth_login(self, user_login_data: UserLogin):
        async with self.session.begin():
            user_data = await self.repository.get_user_by_email(user_login_data.email)
            if not verify_hashed_password(user_login_data.password, user_data.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Email or Password",
                )
            return user_data
