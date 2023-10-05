from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from shop_be import __version__
from shop_be.api.dependencies.db import get_db_session
from shop_be.schemas.base import HealthSchema, VersionSchema

router = APIRouter()


@router.get(
    '/health',
    summary='Health check',
    status_code=HTTPStatus.OK,
    response_model=HealthSchema,
    responses={
        200: {'model': HealthSchema},
        500: {'model': HealthSchema},
    }
)
async def health(db_session: AsyncSession = Depends(get_db_session)) -> HealthSchema:
    """Shows status of the server"""
    await db_session.execute(select(1))
    return HealthSchema(db=db_session.is_active)


@router.get(
    '/version',
    summary='API version',
    response_model=VersionSchema,
)
async def version() -> VersionSchema:
    """Get G50 Transaction version"""
    return VersionSchema(version=__version__)
