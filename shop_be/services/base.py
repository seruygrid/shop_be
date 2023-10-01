import datetime
from typing import TYPE_CHECKING, Generic, Type, Sequence, Dict, Optional, List, TypeVar

from sqlalchemy import select, update, exists, Select
from sqlalchemy.orm import Query

from db_models.db_models import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar('ModelT', bound=Base)


class BaseService(Generic[ModelT]):
    MODEL: Type[ModelT] = Base

    def __init__(self, session: 'AsyncSession'):
        self.session = session

    async def fetch_one(self, filters: Sequence, options: Sequence = ()) -> Optional[ModelT]:
        """Fetch one obj from database"""
        query = select(self.MODEL).filter(*filters).options(*options).limit(1)
        return await self.session.scalar(query)

    async def fetch_all(self, query: Query | Select) -> List[ModelT]:
        """Fetch filtered obj from database"""
        return (await self.session.scalars(query)).all()

    async def update(self, filters: Sequence, values: Dict) -> None:
        """Update instance in DB"""
        now = datetime.datetime.now(tz=None)
        if hasattr(self.MODEL, 'updated'):
            values['updated'] = now
        query = update(self.MODEL).where(*filters).values(**values).execution_options(synchronize_session='fetch')
        await self.session.execute(query)

    async def update_obj(self, obj: ModelT, values: Dict) -> ModelT:
        """Update obj in DB and return obj"""
        await self.update(filters=(self.MODEL.id == obj.id,), values=values)
        obj.__dict__.update(values)
        await self.session.commit()
        return obj

    async def insert(self, values: Dict) -> Base:
        """Insert new obj to DB"""
        return await self.insert_obj(self.MODEL(**values))

    async def insert_obj(self, obj: Base) -> Base:
        """Insert new obj to DB"""
        now = datetime.datetime.now(tz=None)
        if hasattr(self.MODEL, 'created'):
            obj.created = now
        if hasattr(self.MODEL, 'updated'):
            obj.updated = now
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def exist(self, filters: Sequence) -> bool:
        """Check if obj record exists in DB"""
        query = exists(self.MODEL).where(*filters).select()
        return await self.session.scalar(query)
