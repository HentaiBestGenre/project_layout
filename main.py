from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging
from uuid import uuid4
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4

from app.middleware import RouterLoggingMiddleware
from app.core.config import settings
from app.routes import routes


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['X-Requested-With', 'X-Request-ID'],
    expose_headers=['X-Request-ID']
)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name='X-Request-ID',
    update_request_header=True,
    generator=lambda: uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a
)
app.add_middleware(RouterLoggingMiddleware, logger=logging.getLogger(__name__))

app.include_router(routes, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
