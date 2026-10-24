from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate):
        stmnt = insert(User).values(user.model_dump()).returning(User)

        row = await self.session.execute(stmnt)

        row = row.scalar_one_or_none()

        return row

    async def get_user_by_email(self, email):
        stmnt = select(User).where(User.email == email)

        row = await self.session.execute(stmnt)

        row = row.scalar_one_or_none()

        return row
