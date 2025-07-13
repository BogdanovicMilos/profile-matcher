from __future__ import annotations

from sqlalchemy.orm import declarative_base

from infrastructure.database.connection import async_session_maker


Base = declarative_base()


async def async_get_db():
    """
    Dependency for retrieving an async database session.
    Ensures proper cleanup of the session after use.
    """

    _session_maker = async_session_maker()
    async with _session_maker() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
