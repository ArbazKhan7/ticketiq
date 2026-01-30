from sqlalchemy import text
from app.core.db import engine

with engine.connect() as conn:
    result = conn.execute(text("select 1"))
    print(result.scalar())

