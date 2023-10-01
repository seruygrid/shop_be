from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

async_session = sessionmaker(None, expire_on_commit=False, class_=AsyncSession)
session_factory = sessionmaker(None)

Session = scoped_session(session_factory)
