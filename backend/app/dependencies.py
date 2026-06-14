from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID, NAMESPACE_URL, uuid5

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.crud.users import get_user_by_id
from app.utils.auth import decode_access_token


engine = create_async_engine(settings.DATABASE_URL, pool_size=20, max_overflow=10)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


@dataclass
class User:
    id: UUID
    clerk_id: str | None
    email: str
    full_name: str | None = None
    onboarding_completed: bool = False


DEV_USER_ID = uuid5(NAMESPACE_URL, "applypilot.ai/dev-user")


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    """Try local JWT first. If configured and available, Clerk may be used instead.

    Fallback behaviour:
    - In development, return a dev user.
    - If Authorization contains a local JWT (signed with `JWT_SECRET_KEY`) we decode and load the user.
    - Otherwise, if `USE_CLERK` is True and Clerk keys are configured, Clerk verification can be added.
    """
    auth_header = request.headers.get("Authorization", "")
    if settings.APP_ENV == "development":
        return User(
            id=DEV_USER_ID,
            clerk_id="dev_user",
            email="dev@applypilot.ai",
            full_name="Dev User",
            onboarding_completed=True,
        )

    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authentication")

    token = auth_header.replace("Bearer ", "")

    # 1) Try local JWT
    payload = decode_access_token(token)
    if payload and "sub" in payload:
        user = await get_user_by_id(db, payload["sub"])
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token user")
        return User(
            id=user.id,
            clerk_id=user.clerk_id,
            email=user.email,
            full_name=user.full_name,
            onboarding_completed=user.onboarding_completed,
        )

    # 2) Clerk path (not implemented here) — if USE_CLERK is enabled the project should
    # implement Clerk JWT verification (JWKS) or server-side token introspection.
    if settings.USE_CLERK and settings.CLERK_SECRET_KEY:
        raise HTTPException(status_code=501, detail="Clerk verification not implemented on this backend; enable local auth or add Clerk verification logic")

    raise HTTPException(status_code=401, detail="Invalid authentication token")
