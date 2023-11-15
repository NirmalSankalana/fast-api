from fastapi import APIRouter, Depends, status, HTTPException, Response, APIRouter


from ..schemas import vote_schema


router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote():
    