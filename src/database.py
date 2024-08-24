from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import settings

DATABASE_URL = str(settings.DATABASE_ASYNC_URL)

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    pool_recycle=settings.DATABASE_POOL_TTL,
    pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(
        bind=async_engine,  # type: ignore
        class_=AsyncSession,
        expire_on_commit=False,
    )  # type: ignore
    async with async_session() as session:  # type: ignore
        yield session  # type: ignore
