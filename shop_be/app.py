import logging

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.middleware.cors import CORSMiddleware

from db_models.db_models import metadata
from shop_be.conf.db import async_session
from shop_be.conf.settings import settings, Settings
from shop_be.api import settings as api_settings, base, types, categories, products, shops, orders
from shop_be.exception_handlers import init_exception_handlers

logger = logging.getLogger(__name__)


def init_routes(app: 'FastAPI') -> None:
    """Connect routes to app"""
    app.include_router(base.router, tags=['Base'], prefix='/api')
    app.include_router(types.router, tags=['Types'], prefix='/api')
    app.include_router(shops.router, tags=['Shops'], prefix='/api')
    app.include_router(orders.router, tags=['Orders'], prefix='/api')
    app.include_router(products.router, tags=['Products'], prefix='/api')
    app.include_router(categories.router, tags=['Categories'], prefix='/api')
    app.include_router(api_settings.router, tags=['Settings'], prefix='/api')


def init_middlewares(app: FastAPI, app_settings: Settings):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def init_db(app_settings: Settings):
    """Init database"""
    engine = create_async_engine(app_settings.sqlalchemy_database_uri)
    async_session.configure(bind=engine)
    metadata.bind = engine


def create_app(app_settings: Settings | None = None) -> 'FastAPI':
    """Create app with including configurations"""
    app_settings = app_settings if app_settings is not None else settings
    init_db(app_settings)
    app = FastAPI(
        title='Harvest HUB Shop',
        debug=app_settings.DEBUG,
        docs_url='/api/docs',
        redoc_url='/api/redoc',
    )
    init_middlewares(app, app_settings)
    init_exception_handlers(app)
    init_routes(app)
    return app
