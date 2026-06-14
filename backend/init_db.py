import asyncio
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.dependencies import engine
from app.models import Base

async def init_database():
    print("Connecting to database and creating tables...")
    try:
        async with engine.begin() as conn:
            # Drop all tables if you want to start fresh or keep them
            # We run run_sync on create_all to create any missing tables
            await conn.run_sync(Base.metadata.create_all)
        print("\nSUCCESS: All PostgreSQL tables created successfully on Neon!")
    except Exception as e:
        import traceback
        print("\nERROR initializing database:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(init_database())
