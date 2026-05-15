import os
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.bingo_routes import router as bingo_router
from app.routes.websocket_routes import router as websocket_router


def get_base_path():

    if getattr(sys, "frozen", False):

        return sys._MEIPASS

    return os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )


BASE_PATH = get_base_path()

STATIC_DIR = os.path.join(
    BASE_PATH,
    "app",
    "static"
)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

app.include_router(bingo_router)

app.include_router(websocket_router)