from fastapi import Query
from pydantic import BaseModel


class VersionSchema(BaseModel):
    """Version response schema"""
    version: str


class HealthSchema(BaseModel):
    """Health response schema"""
    db: bool


class BaseNotAuthSchema(BaseModel):
    """Base error schema for not authenticated clients"""
    detail: str


class OKSchema(BaseModel):
    """Base OK schema"""
    OK: bool = True


class Pagination(BaseModel):
    """Pagination parameters"""
    skip: int = Query(0)
    limit: int = Query(25, lt=100)


class LoggerDataSchema(BaseModel):
    """Logger data schema"""
    message: str
    client_id: int | None = None
    transaction_id: int | None = None
    pool_transaction_id: int | None = None
