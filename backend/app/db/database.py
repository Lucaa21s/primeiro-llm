import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Resolução Dinâmica de Host para funcionar tanto no Docker quanto Local
raw_url = os.getenv("DATABASE_URL", "postgresql://ai:ai@localhost:5432/ai_memory")
DATABASE_URL_SYNC = raw_url

# Ajusta a URL para o driver do asyncpg
if raw_url.startswith("postgresql://"):
    DATABASE_URL_ASYNC = raw_url.replace("postgresql://", "postgresql+asyncpg://")
else:
    DATABASE_URL_ASYNC = "postgresql+asyncpg://ai:ai@localhost:5432/ai_memory"

# Engine Síncrono (mantido para compatibilidade e init_db)
sync_engine = create_engine(DATABASE_URL_SYNC)

# Engine Assíncrono (Para FastAPI e alta concorrência)
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
