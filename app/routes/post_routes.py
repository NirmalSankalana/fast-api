from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..schemas import post_schema
from .. import models
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", response_model=List[post_schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    # Convert the data to a format that can be easily serialized to JSON
    serialized_results = []
    for post, vote_count in results:
        serialized_result = {
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "published": post.published,
                "owner": post.owner_id,
                "created_at": post.created_at.isoformat(),
                # Add other fields as needed
            },
            "votes": vote_count
        }
        serialized_results.append(serialized_result)

    return JSONResponse(content=serialized_results)


@router.get("/{id}", response_model=post_schema.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exists.")
    return post


@router.get("/latest", response_model=post_schema.Post)
def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).one()
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=post_schema.Post)
def create_posts(post: post_schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    # ** - unpacked the dictionary to the base class
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post.owner_id, current_user.id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exists.")
    if int(post.owner_id) != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post_query.delete(synchronize_session=False)
    db.commit()
    print(f"Succesfully deleted post {id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=post_schema.Post)
def update_post(id: int, post: post_schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_one = post_query.first()
    if post_one == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exists.")
    if int(post_one.owner_id) != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
