from sqlalchemy import Column, Integer, String, Float, DateTime, Text, event
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# ── Database URL with SQLite fallback ─────────────────────────────────────────
# PostgreSQL is preferred. If not configured/available, falls back to SQLite.

_POSTGRES_URL = os.getenv("DATABASE_URL", "")
_SQLITE_URL   = "sqlite+aiosqlite:///./automech.db"

# Detect if user has set a real postgres URL
if _POSTGRES_URL and "postgresql" in _POSTGRES_URL and "yourpassword" not in _POSTGRES_URL and "password@" not in _POSTGRES_URL.replace("yourpassword", ""):
    DATABASE_URL = _POSTGRES_URL
    IS_SQLITE = False
else:
    DATABASE_URL = _SQLITE_URL
    IS_SQLITE = True
    if not _POSTGRES_URL or "postgresql" not in _POSTGRES_URL:
        print("ℹ️  DATABASE_URL not set → using SQLite (automech.db). Set DATABASE_URL in .env for PostgreSQL.")
    else:
        print("ℹ️  PostgreSQL URL looks unconfigured → using SQLite fallback.")

# ── Engine ────────────────────────────────────────────────────────────────────
_engine_kwargs = {"echo": False}
if IS_SQLITE:
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_async_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# ── Models ─────────────────────────────────────────────────────────────────────

class VehicleProfile(Base):
    __tablename__ = "vehicle_profiles"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    make       = Column(String, nullable=False)
    model      = Column(String, nullable=False)
    year       = Column(Integer, nullable=False)
    mileage    = Column(Float, nullable=True)
    fuel_type  = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DiagnosticHistory(Base):
    __tablename__ = "diagnostic_history"

    id         = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, nullable=False)
    symptoms   = Column(Text, nullable=False)
    diagnosis  = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String, unique=True, nullable=False, index=True)
    email         = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name     = Column(String, nullable=True)
    is_active     = Column(Integer, default=1)  # SQLite doesn't have boolean
    created_at    = Column(DateTime, default=datetime.utcnow)
    last_login    = Column(DateTime, nullable=True)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id         = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False, index=True)  # Links messages in same conversation
    vehicle_id = Column(Integer, nullable=True)  # Optional link to vehicle
    role       = Column(String, nullable=False)  # 'user' or 'assistant'
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ── Lifecycle ─────────────────────────────────────────────────────────────────

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"✅ Database ready ({'SQLite' if IS_SQLITE else 'PostgreSQL'})")


async def get_db():
    async with SessionLocal() as session:
        yield session
