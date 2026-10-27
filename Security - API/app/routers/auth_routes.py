from fastapi import APIRouter, Depends, status, Security
from typing import Annotated
from app.dependencies import get_current_user, get_user_service
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_auth_service import UserAuthService

from fastapi.security import OAuth2PasswordRequestForm

route = APIRouter(prefix="/auth", tags=["Authentication"])

User_Service = Annotated[UserAuthService, Depends(get_user_service)]


@route.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def auth_signup(user: UserCreate, service: User_Service):

    return await service.auth_signup(user)


@route.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def auth_login(
    service: User_Service,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await service.auth_login(form_data)


@route.get("/user", response_model=UserResponse)
async def get_user_profile(
    current_user: Annotated[
        UserResponse, Security(get_current_user, scopes=["current_user"])
    ],
):
    return current_user
