from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

print(settings.database_password)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

my_posts = [{"title": "title of blog 1", "content": "content of blog 1", "id": 1},
            {"title": "favourite stretches", "content": "I like child pose", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def read_root():
    return {"Hello": "Welcome to my api"}
