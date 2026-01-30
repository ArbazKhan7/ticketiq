from sqlalchemy import create_engine
from app.core.config import settings

# SQLAlchemy engine (Supabase Postgres)
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)
