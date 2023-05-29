from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


try:
    conn = psycopg2.connect(host="localhost", database="fastapi",
                            user='postgres', password="azOLe@123", cursor_factory=RealDictCursor)
    cursor = conn.cursor
    print("Database connection was successfull")
except Exception as error:
    print("Connecting to database failed.")
    print("Error: ", error)


my_posts = [{"title": "title of post 1",
             "content": "content of post 1", "id": 123}, {"title": "title of post 2", "content": "content of post 2", "id": 213}]


def find_post(id):
    for p in my_posts:
        if p["id"] == int(id):
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    # Fast API automatically convert this dictionary to JSON
    return {"message": "Welcome to API!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{:id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found.")
    print(post)
    return {"post_detail": post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = random.randint(1, 100000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{:id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exists.")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{:id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exists.")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
