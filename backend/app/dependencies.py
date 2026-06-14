from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID, NAMESPACE_URL, uuid5
import httpx
from jose import jwt

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select

from app.config import settings
from app.crud.users import get_user_by_id
from app.utils.auth import decode_access_token

connect_args = {"ssl": True} if "neon.tech" in settings.DATABASE_URL else {}
engine = create_async_engine(settings.DATABASE_URL, pool_size=20, max_overflow=10, connect_args=connect_args)
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


async def get_clerk_user_info(clerk_user_id: str) -> dict | None:
    if not settings.CLERK_SECRET_KEY:
        return None
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.clerk.com/v1/users/{clerk_user_id}",
                headers={"Authorization": f"Bearer {settings.CLERK_SECRET_KEY}"}
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
    return None


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    """Try local JWT first, check Clerk JWT, or fallback to dev user in development if no token is sent."""
    auth_header = request.headers.get("Authorization", "")
    
    if settings.APP_ENV == "development" and not auth_header:
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

    # 1. Try decoding as Clerk token
    clerk_id = None
    email_claim = None
    try:
        claims = jwt.get_unverified_claims(token)
        if claims and "sub" in claims and claims["sub"].startswith("user_"):
            clerk_id = claims["sub"]
            email_claim = claims.get("email")
    except Exception:
        pass

    if clerk_id:
        from app.models import User as DBUser
        # Sync/Find User in PostgreSQL database
        stmt = select(DBUser).where((DBUser.clerk_id == clerk_id) | (DBUser.email == (email_claim or "")))
        result = await db.execute(stmt)
        db_user = result.scalars().first()

        if not db_user:
            # Retrieve details from Clerk Backend API
            clerk_info = await get_clerk_user_info(clerk_id)
            if not clerk_info:
                # If Clerk verification failed or key is incorrect, we can fallback to claims if available
                if email_claim:
                    email = email_claim
                    full_name = "Clerk User"
                else:
                    raise HTTPException(status_code=401, detail="Unable to verify Clerk user")
            else:
                email_addresses = clerk_info.get("email_addresses", [])
                email = email_addresses[0].get("email_address") if email_addresses else f"{clerk_id}@applypilot.ai"
                first_name = clerk_info.get("first_name") or ""
                last_name = clerk_info.get("last_name") or ""
                full_name = f"{first_name} {last_name}".strip() or "Clerk User"

            # Register user in local Neon DB
            db_user = DBUser(
                clerk_id=clerk_id,
                email=email,
                full_name=full_name,
                onboarding_completed=False
            )
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)

        return User(
            id=db_user.id,
            clerk_id=db_user.clerk_id,
            email=db_user.email,
            full_name=db_user.full_name,
            onboarding_completed=db_user.onboarding_completed,
        )

    # 2. Try local JWT fallback
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

    raise HTTPException(status_code=401, detail="Invalid authentication token")
