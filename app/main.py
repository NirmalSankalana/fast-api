from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user='postgres', password="azOLe@123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break

    except Exception as error:
        print("Connecting to database failed.")
        print("Error: ", error)
        time.sleep(2)


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
    cursor.execute("""SELECT * FROM posts; """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.get("/posts/{:id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found.")
    print(post)
    return {"post_detail": post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.delete("/posts/{:id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    print(f"Succesfully deleted post {id}")
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exists.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{:id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exists.")
    return {"data": updated_post}
