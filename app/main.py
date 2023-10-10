from fastapi import FastAPI
from fastapi.params import Body

from . import models
from .database import engine, get_db
from .routes import post_routes, user_routes, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to API!!!"}

app.include_router(post_routes.router)
app.include_router(user_routes.router)
app.include_router(auth.router)
