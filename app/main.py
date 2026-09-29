from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import STATIC_DIR
from .routes import router


app = FastAPI(

    title=
        "ComicCraft - AI Comic Story Creator",

    version="1.0.0",

    description=
        "Generate comic stories and illustrations using Gemini and Stable Diffusion."
)


app.mount(

    "/static",

    StaticFiles(
        directory=str(
            STATIC_DIR
        )
    ),

    name="static"
)


app.include_router(
    router
)