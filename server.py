import uvicorn

from shop_be.app import create_app
from shop_be.conf.settings import settings

app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=settings.PORT,
        loop='uvloop'
    )
