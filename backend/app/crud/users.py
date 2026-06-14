from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    q = select(User).where(User.email == email)
    res = await db.execute(q)
    return res.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    q = select(User).where(User.id == user_id)
    res = await db.execute(q)
    return res.scalars().first()


async def get_user_by_clerk_id(db: AsyncSession, clerk_id: str) -> User | None:
    q = select(User).where(User.clerk_id == clerk_id)
    res = await db.execute(q)
    return res.scalars().first()


async def create_user(db: AsyncSession, email: str, password: str | None = None, full_name: str | None = None, clerk_id: str | None = None) -> User:
    hashed = pwd_context.hash(password) if password else None
    user = User(email=email, full_name=full_name, hashed_password=hashed, clerk_id=clerk_id)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
