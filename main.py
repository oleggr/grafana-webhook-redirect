import os

from fastapi import FastAPI, Request, Response

from app.routers import direct, by_token
from app.middleware.handler import event_handler, log


prefix = os.getenv('API_PREFIX', '/grafana/events')


app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):

    await log.exception(exc)

    await log.info(
        await request.body()
    )

    return Response(
        status_code=400
    )


app.event_handler = event_handler

app.include_router(
    direct.router, prefix=prefix
)

app.include_router(
    by_token.router, prefix=prefix
)
