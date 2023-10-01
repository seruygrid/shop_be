import logging
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from shop_be import exceptions

logger = logging.getLogger(__name__)


async def does_not_exist_exception_handler(request: Request, exc: exceptions.DoesNotExistException) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc)),
    )


async def validation_exception_handler(request: Request, exc: exceptions.ValidationException) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(exc)),
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(exceptions.DoesNotExistException)(does_not_exist_exception_handler)
    app.exception_handler(exceptions.ValidationException)(validation_exception_handler)
