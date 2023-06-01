from fastapi import FastAPI
from fastapi.params import Body

from . import models
from .database import engine, get_db
from .routes import post_routes, user_routes


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
async def root():
    # Fast API automatically convert this dictionary to JSON
    return {"message": "Welcome to API!!!"}

# Mount the routes from the separate files
app.include_router(post_routes.router)
app.include_router(user_routes.router)
