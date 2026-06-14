from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.schemas import AuthMeResponse, SignupRequest, LoginRequest, TokenResponse
from app.crud.users import get_user_by_email, create_user, verify_password
from app.utils.auth import create_access_token

router = APIRouter()


@router.get("/me")
async def get_me(user=Depends(get_current_user)) -> AuthMeResponse:
    return AuthMeResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        onboarding_completed=user.onboarding_completed,
    )


@router.post("/signup", response_model=TokenResponse)
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await create_user(db, email=data.email, password=data.password, full_name=data.full_name)
    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, data.email)
    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token)
