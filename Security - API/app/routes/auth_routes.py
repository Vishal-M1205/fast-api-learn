from fastapi import APIRouter, Depends, status
from typing import Annotated
from app.dependencies import get_user_service
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.service.user_auth_service import UserAuthService

route = APIRouter(prefix="/auth", tags=["Authentication"])

User_Service = Annotated[UserAuthService, Depends(get_user_service)]


@route.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def auth_signup(user: UserCreate, service: User_Service):

    return await service.auth_signup(user)


@route.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def auth_login(user: UserLogin, service: User_Service):
    return await service.auth_login(user)
