import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1.endpoints import router
from src.core.config import settings
from src.db.init_db import add_test_data
from src.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    await init_db()
    try:
        await add_test_data()
    except Exception as e:
        print(e)
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    description=settings.project_description,
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(router)

if __name__ == '__main__':
    logging.info(msg='Starting billing service')
    uvicorn.run(
        'main:app',
        host='0.0.0.0',  # noqa: S104
        port=8000,
    )
