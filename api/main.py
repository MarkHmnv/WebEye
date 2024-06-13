from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.auth.router import auth_router
from api.monitoring.router import monitoring_router
from user.router import user_router


def include_routers(app: FastAPI, routers: tuple[APIRouter]):
    for router in routers:
        app.include_router(router, prefix='/api/v1')


app = FastAPI()

routers = (
    auth_router,
    user_router,
    monitoring_router
)
include_routers(app, routers)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    import asyncio
    import uvicorn
    from api.core.database import create_tables

    asyncio.run(create_tables())
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)